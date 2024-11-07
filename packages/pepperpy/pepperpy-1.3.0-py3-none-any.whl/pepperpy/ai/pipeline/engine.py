import asyncio
import logging
from dataclasses import dataclass
from typing import Any, AsyncIterator, Dict, List


@dataclass
class PipelineStage:
    """Single stage in pipeline"""

    name: str
    handler: callable
    config: Dict[str, Any] = None
    retry_count: int = 3
    timeout: float = None


class PipelineEngine:
    """Efficient pipeline execution engine"""

    def __init__(self, stages: List[PipelineStage]):
        self.stages = stages
        self.logger = logging.getLogger("pipeline")

    async def process(self, data: Any, context: Dict[str, Any] = None) -> AsyncIterator[Any]:
        """Process data through pipeline"""
        context = context or {}
        current = data

        for stage in self.stages:
            try:
                # Execute stage with retries
                for attempt in range(stage.retry_count):
                    try:
                        if stage.timeout:
                            current = await asyncio.wait_for(
                                stage.handler(current, context), timeout=stage.timeout
                            )
                        else:
                            current = await stage.handler(current, context)
                        break
                    except Exception as e:
                        self.logger.warning(
                            f"Stage {stage.name} failed (attempt {attempt + 1}): {str(e)}"
                        )
                        if attempt == stage.retry_count - 1:
                            raise
                        await asyncio.sleep(2**attempt)  # Exponential backoff

                yield current

            except Exception as e:
                self.logger.error(f"Pipeline failed at stage {stage.name}: {str(e)}")
                raise
