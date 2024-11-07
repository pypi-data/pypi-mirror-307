from dataclasses import dataclass

import torch
from transformers import PreTrainedModel


@dataclass
class SpeculativeConfig:
    """Configuration for speculative decoding"""

    draft_model_name: str
    num_draft_tokens: int = 5
    max_new_tokens: int = 100
    temperature: float = 0.7


class SpeculativeDecoder:
    """Speculative decoding for faster generation"""

    def __init__(
        self,
        target_model: PreTrainedModel,
        draft_model: PreTrainedModel,
        config: SpeculativeConfig,
    ):
        self.target_model = target_model
        self.draft_model = draft_model
        self.config = config

    async def generate(
        self, input_ids: torch.Tensor, attention_mask: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        """Generate with speculative decoding"""
        current_ids = input_ids
        current_mask = attention_mask

        for _ in range(0, self.config.max_new_tokens, self.config.num_draft_tokens):
            # Generate draft tokens
            draft_outputs = await self._generate_draft(current_ids, current_mask)

            # Verify with target model
            target_outputs = await self._verify_draft(current_ids, current_mask, draft_outputs)

            # Accept verified tokens
            current_ids = torch.cat([current_ids, target_outputs], dim=-1)
            current_mask = torch.ones_like(current_ids)

            # Check for end condition
            if self._is_finished(target_outputs):
                break

        return current_ids

    async def _generate_draft(
        self, input_ids: torch.Tensor, attention_mask: torch.Tensor
    ) -> torch.Tensor:
        """Generate draft tokens quickly"""
        with torch.inference_mode():
            outputs = self.draft_model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=self.config.num_draft_tokens,
                temperature=self.config.temperature,
                do_sample=True,
            )
        return outputs[:, input_ids.size(1) :]

    async def _verify_draft(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        draft_tokens: torch.Tensor,
    ) -> torch.Tensor:
        """Verify draft tokens with target model"""
        with torch.inference_mode():
            # Get target model probabilities
            target_outputs = self.target_model(
                input_ids=torch.cat([input_ids, draft_tokens], dim=-1),
                attention_mask=torch.ones_like(torch.cat([input_ids, draft_tokens], dim=-1)),
            )

            # Accept tokens that match target distribution
            target_probs = torch.softmax(
                target_outputs.logits[:, input_ids.size(1) - 1 : -1], dim=-1
            )
            draft_probs = torch.softmax(
                self.draft_model(input_ids=input_ids, attention_mask=attention_mask).logits[:, -1:],
                dim=-1,
            )

            # Compare distributions
            kl_div = torch.nn.functional.kl_div(draft_probs.log(), target_probs, reduction="none")

            # Accept tokens with low divergence
            accepted_mask = (kl_div.mean(dim=-1) < 0.5).float()
            return draft_tokens * accepted_mask.unsqueeze(-1)

    def _is_finished(self, outputs: torch.Tensor) -> bool:
        """Check if generation should stop"""
        return bool((outputs == self.target_model.config.eos_token_id).any())
