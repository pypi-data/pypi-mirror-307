from dataclasses import dataclass
from typing import Dict, List, Optional

from .planner import QueryPlan, QueryType


@dataclass
class GenerationConfig:
    """Configuration for answer generation"""

    max_context_length: int = 2000
    temperature: float = 0.7
    use_few_shot: bool = True
    num_examples: int = 2
    stream_output: bool = False


class AnswerGenerator:
    """Generate answers using retrieved context"""

    def __init__(self, config: GenerationConfig) -> None:
        self.config = config
        self._prompt_templates = {
            QueryType.FACTUAL: """
            Answer the question based on the provided context.
            If the context doesn't contain enough information, say so.

            Context:
            {{ context }}

            Question: {{ question }}

            Answer:
            """,
            QueryType.ANALYTICAL: """
            Analyze the following question using the provided context.
            Explain your reasoning and cite relevant information.

            Context:
            {{ context }}

            Question: {{ question }}

            Analysis:
            """,
            QueryType.COMPARATIVE: """
            Compare the following aspects based on the provided context.
            Highlight key similarities and differences.

            Context:
            {{ context }}

            Compare: {{ question }}

            Comparison:
            """,
        }

    async def generate_answer(
        self,
        query: str,
        context: List[str],
        plan: QueryPlan,
        examples: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """Generate answer based on context and plan"""
        # Format context
        formatted_context = self._format_context(context, plan)

        # Get prompt template
        template = self._prompt_templates.get(
            plan.query_type, self._prompt_templates[QueryType.FACTUAL]
        )

        # Add examples if enabled
        if self.config.use_few_shot and examples:
            template = self._add_examples(template, examples)

        # Generate answer
        prompt = template.replace("{{ context }}", formatted_context).replace(
            "{{ question }}", query
        )

        return await self._generate(prompt)

    def _format_context(self, context: List[str], plan: QueryPlan) -> str:
        """Format context based on query plan"""
        # Truncate to max length
        total_length = 0
        selected_chunks = []

        for chunk in context:
            chunk_length = len(chunk)
            if total_length + chunk_length > self.config.max_context_length:
                break
            selected_chunks.append(chunk)
            total_length += chunk_length

        # Format based on query type
        if plan.query_type == QueryType.COMPARATIVE:
            # Group context by comparison targets
            groups = self._group_comparative_context(selected_chunks, plan)
            return "\n\nComparing:\n" + "\n\nvs\n\n".join(groups)

        elif plan.query_type == QueryType.ANALYTICAL:
            # Add section headers
            return (
                "\n\nBackground:\n"
                + "\n\nKey Points:\n".join(selected_chunks[:3])
                + "\n\nAnalysis:\n"
                + "\n\n".join(selected_chunks[3:])
            )

        return "\n\n".join(selected_chunks)

    def _group_comparative_context(self, chunks: List[str], plan: QueryPlan) -> List[str]:
        """Group context for comparative queries"""
        if len(plan.sub_queries) < 2:
            return ["\n\n".join(chunks)]

        # Group chunks by relevance to each sub-query
        groups = []
        for sub_query in plan.sub_queries:
            relevant_chunks = [chunk for chunk in chunks if self._is_relevant(chunk, sub_query)]
            groups.append("\n\n".join(relevant_chunks))

        return groups

    def _is_relevant(self, text: str, query: str) -> bool:
        """Check if text is relevant to query"""
        # Simple relevance check - can be enhanced
        query_terms = set(query.lower().split())
        text_terms = set(text.lower().split())
        return bool(query_terms & text_terms)

    def _add_examples(self, template: str, examples: List[Dict[str, str]]) -> str:
        """Add few-shot examples to template"""
        examples_text = "\nExamples:\n"
        for example in examples[: self.config.num_examples]:
            examples_text += f"\nQuestion: {example['question']}\n"
            examples_text += f"Answer: {example['answer']}\n"
        return examples_text + "\n" + template

    async def _generate(self, prompt: str) -> str:
        """Generate text using language model"""
        # Implementation depends on specific LLM being used
        raise NotImplementedError()
