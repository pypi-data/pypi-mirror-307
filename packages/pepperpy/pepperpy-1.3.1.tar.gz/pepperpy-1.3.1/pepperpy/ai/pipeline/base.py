import asyncio
import logging
from dataclasses import dataclass
from typing import Any, AsyncIterator, Callable, Dict, List, Optional


@dataclass
class PipelineStep:
    """Represents a step in the pipeline"""

    name: str
    function: Callable
    config: Optional[Dict[str, Any]] = None
    retry_count: int = 3
    timeout: Optional[float] = None


class Pipeline:
    """Data pipeline for AI operations"""

    def __init__(self, name: str):
        self.name = name
        self.steps: List[PipelineStep] = []
        self.logger = logging.getLogger(f"pipeline.{name}")

    def add_step(
        self,
        name: str,
        function: Callable,
        config: Optional[Dict[str, Any]] = None,
        retry_count: int = 3,
        timeout: Optional[float] = None,
    ) -> "Pipeline":
        """Add a step to the pipeline"""
        step = PipelineStep(
            name=name,
            function=function,
            config=config,
            retry_count=retry_count,
            timeout=timeout,
        )
        self.steps.append(step)
        return self

    async def execute(self, data: Any) -> AsyncIterator[Any]:
        """Execute pipeline steps"""
        current_data = data

        for step in self.steps:
            self.logger.info(f"Executing step: {step.name}")

            for attempt in range(step.retry_count):
                try:
                    if step.timeout:
                        # Execute with timeout
                        current_data = await asyncio.wait_for(
                            step.function(current_data, **(step.config or {})),
                            timeout=step.timeout,
                        )
                    else:
                        current_data = await step.function(current_data, **(step.config or {}))
                    break
                except Exception as e:
                    self.logger.error(f"Step {step.name} failed (attempt {attempt + 1}): {str(e)}")
                    if attempt == step.retry_count - 1:
                        raise
                    await asyncio.sleep(2**attempt)  # Exponential backoff

            yield current_data
