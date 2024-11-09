import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List


class QueryType(Enum):
    """Types of queries for specialized handling"""

    FACTUAL = "factual"
    ANALYTICAL = "analytical"
    COMPARATIVE = "comparative"
    CAUSAL = "causal"
    PROCEDURAL = "procedural"


@dataclass
class QueryPlan:
    """Plan for processing a query"""

    query_type: QueryType
    sub_queries: List[str]
    required_context: List[str]
    constraints: Dict[str, Any]
    metadata: Dict[str, Any]


class QueryPlanner:
    """Plan query processing strategy"""

    def __init__(self) -> None:
        self._type_patterns = {
            QueryType.FACTUAL: r"what|who|when|where",
            QueryType.ANALYTICAL: r"why|how|analyze|explain",
            QueryType.COMPARATIVE: r"compare|difference|versus|vs",
            QueryType.CAUSAL: r"cause|effect|impact|result",
            QueryType.PROCEDURAL: r"steps|process|procedure|method",
        }

    def create_plan(self, query: str) -> QueryPlan:
        """Create execution plan for query"""
        # Determine query type
        query_type = self._detect_type(query)

        # Break into sub-queries if needed
        sub_queries = self._create_sub_queries(query, query_type)

        # Identify required context
        required_context = self._identify_context(query)

        # Define constraints
        constraints = self._get_constraints(query_type)

        return QueryPlan(
            query_type=query_type,
            sub_queries=sub_queries,
            required_context=required_context,
            constraints=constraints,
            metadata={"original_query": query},
        )

    def _detect_type(self, query: str) -> QueryType:
        """Detect query type based on patterns"""
        query = query.lower()

        for qtype, pattern in self._type_patterns.items():
            if re.search(pattern, query):
                return qtype

        return QueryType.FACTUAL  # Default type

    def _create_sub_queries(self, query: str, query_type: QueryType) -> List[str]:
        """Break query into sub-queries if needed"""
        if query_type == QueryType.COMPARATIVE:
            # Split comparative queries
            parts = re.split(r"compare|versus|vs", query, flags=re.IGNORECASE)
            return [part.strip() for part in parts if part.strip()]

        elif query_type == QueryType.ANALYTICAL:
            # Create context and analysis queries
            return [
                f"What are the key facts about {query}?",
                f"How do these facts relate to {query}?",
                f"What conclusions can be drawn about {query}?",
            ]

        return [query]

    def _identify_context(self, query: str) -> List[str]:
        """Identify required context categories"""
        context = []

        # Add basic context
        context.append("background")

        # Add specific context based on query
        if "history" in query.lower():
            context.append("historical")
        if "future" in query.lower():
            context.append("predictive")
        if "problem" in query.lower():
            context.append("problem-solving")

        return context

    def _get_constraints(self, query_type: QueryType) -> Dict[str, Any]:
        """Get constraints based on query type"""
        constraints = {"max_context_chunks": 5, "min_similarity": 0.7}

        if query_type == QueryType.FACTUAL:
            constraints.update({"max_context_chunks": 3, "min_similarity": 0.8})
        elif query_type == QueryType.ANALYTICAL:
            constraints.update({"max_context_chunks": 7, "min_similarity": 0.6})

        return constraints
