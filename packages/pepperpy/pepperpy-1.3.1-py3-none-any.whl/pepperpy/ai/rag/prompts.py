import json
from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
from jinja2 import Template


@dataclass
class PromptConfig:
    """Configuration for dynamic prompts"""

    max_context_length: int = 2000
    num_examples: int = 2
    use_few_shot: bool = True
    instruction_template: str = """
    Answer the question based on the provided context.
    If the context doesn't contain enough information, say so.

    Context:
    {{ context }}

    {% if examples %}
    Examples:
    {% for example in examples %}
    Question: {{ example.question }}
    Answer: {{ example.answer }}
    {% endfor %}
    {% endif %}

    Question: {{ question }}

    Answer:
    """


class DynamicPromptOptimizer:
    """Optimize prompts for RAG"""

    def __init__(self, config: PromptConfig) -> None:
        self.config = config
        self.template = Template(config.instruction_template)
        self._example_cache: Dict[str, List[Dict[str, str]]] = {}

    async def optimize_prompt(
        self,
        question: str,
        context: List[str],
        examples: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """Create optimized prompt with context"""
        # Truncate context to fit
        context_text = self._format_context(context)

        # Get relevant examples if enabled
        if self.config.use_few_shot and not examples:
            examples = await self._get_relevant_examples(question)

        # Render prompt
        prompt = self.template.render(
            context=context_text,
            question=question,
            examples=examples[: self.config.num_examples] if examples else None,
        )

        return prompt

    def _format_context(self, context: List[str]) -> str:
        """Format and truncate context"""
        context_text = "\n\n".join(context)

        if len(context_text) > self.config.max_context_length:
            context_text = context_text[: self.config.max_context_length] + "..."

        return context_text

    async def _get_relevant_examples(self, question: str) -> List[Dict[str, str]]:
        """Get relevant few-shot examples"""
        # Load examples if not cached
        if not self._example_cache:
            await self._load_examples()

        # Find similar examples
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")

        question_embedding = model.encode(question)
        example_embeddings = model.encode(
            [ex["question"] for ex in self._example_cache["examples"]]
        )

        # Get most similar examples
        similarities = np.dot(example_embeddings, question_embedding)
        top_indices = np.argsort(similarities)[-self.config.num_examples :]

        return [self._example_cache["examples"][i] for i in top_indices]

    async def _load_examples(self) -> None:
        """Load few-shot examples"""
        # Load from JSON file
        with open("examples.json") as f:
            self._example_cache = json.load(f)
