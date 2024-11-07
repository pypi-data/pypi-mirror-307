from dataclasses import dataclass
from typing import Optional

import torch
import triton
import triton.language as tl


@dataclass
class FlashAttentionConfig:
    """Configuration for Flash Attention 2"""

    head_dim: int = 64
    block_size: int = 128
    num_warps: int = 4
    num_stages: int = 3


@triton.jit
def _flash_attention_kernel(
    q_ptr,
    k_ptr,
    v_ptr,
    o_ptr,
    stride_qz,
    stride_qh,
    stride_qm,
    stride_qk,
    stride_kz,
    stride_kh,
    stride_kn,
    stride_kk,
    stride_vz,
    stride_vh,
    stride_vk,
    stride_vn,
    stride_oz,
    stride_oh,
    stride_om,
    stride_on,
    Z,
    H,
    M,
    N,
    K,
    scaling,
    BLOCK_M: tl.constexpr,
    BLOCK_N: tl.constexpr,
    BLOCK_K: tl.constexpr,
):
    """Optimized Flash Attention 2 kernel"""
    start_m = tl.program_id(0) * BLOCK_M
    start_n = tl.program_id(1) * BLOCK_N

    # Initialize pointers to Q, K, V
    q_block_ptr = tl.make_block_ptr(
        q_ptr,
        (Z, H, M, K),
        (stride_qz, stride_qh, stride_qm, stride_qk),
        (0, 0, start_m, 0),
        (1, 1, BLOCK_M, BLOCK_K),
        (0, 0, 0, 0),
    )
    k_block_ptr = tl.make_block_ptr(
        k_ptr,
        (Z, H, N, K),
        (stride_kz, stride_kh, stride_kn, stride_kk),
        (0, 0, start_n, 0),
        (1, 1, BLOCK_N, BLOCK_K),
        (0, 0, 0, 0),
    )
    v_block_ptr = tl.make_block_ptr(
        v_ptr,
        (Z, H, N, K),
        (stride_vz, stride_vh, stride_vk, stride_vn),
        (0, 0, start_n, 0),
        (1, 1, BLOCK_N, BLOCK_K),
        (0, 0, 0, 0),
    )

    # Load Q, K blocks
    q = tl.load(q_block_ptr)
    k = tl.load(k_block_ptr)

    # Compute attention scores
    scores = tl.dot(q, tl.trans(k))
    scores = scores * scaling

    # Apply softmax
    scores = tl.softmax(scores)

    # Load V block and compute output
    v = tl.load(v_block_ptr)
    output = tl.dot(scores, v)

    # Store output
    o_block_ptr = tl.make_block_ptr(
        o_ptr,
        (Z, H, M, K),
        (stride_oz, stride_oh, stride_om, stride_on),
        (0, 0, start_m, 0),
        (1, 1, BLOCK_M, BLOCK_K),
        (0, 0, 0, 0),
    )
    tl.store(o_block_ptr, output)


class FlashAttention2:
    """Flash Attention 2 implementation"""

    def __init__(self, config: FlashAttentionConfig):
        self.config = config

    def forward(
        self,
        q: torch.Tensor,
        k: torch.Tensor,
        v: torch.Tensor,
        mask: Optional[torch.Tensor] = None,
        scale: Optional[float] = None,
    ) -> torch.Tensor:
        """Forward pass with Flash Attention 2"""
        batch_size, num_heads, seq_len, head_dim = q.shape
        scale = scale or (1.0 / head_dim**0.5)

        # Ensure tensors are contiguous
        q = q.contiguous()
        k = k.contiguous()
        v = v.contiguous()

        # Initialize output
        output = torch.empty_like(q)

        def grid(meta):
            return (
                triton.cdiv(seq_len, meta["BLOCK_M"]),
                triton.cdiv(seq_len, meta["BLOCK_N"]),
            )

        # Launch kernel
        _flash_attention_kernel[grid](
            q,
            k,
            v,
            output,
            q.stride(0),
            q.stride(1),
            q.stride(2),
            q.stride(3),
            k.stride(0),
            k.stride(1),
            k.stride(2),
            k.stride(3),
            v.stride(0),
            v.stride(1),
            v.stride(2),
            v.stride(3),
            output.stride(0),
            output.stride(1),
            output.stride(2),
            output.stride(3),
            batch_size,
            num_heads,
            seq_len,
            seq_len,
            head_dim,
            scale,
            BLOCK_M=self.config.block_size,
            BLOCK_N=self.config.block_size,
            BLOCK_K=head_dim,
            num_warps=self.config.num_warps,
            num_stages=self.config.num_stages,
        )

        return output
