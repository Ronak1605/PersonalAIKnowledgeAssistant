from typing import List
from ingestion.models.chunk import Chunk
from generation.base_generator import BaseGenerator


class SimpleGenerator(BaseGenerator):
    """
    Basic generator that concatenates context.
    (Placeholder for real LLM)
    """

    def generate(self, query: str, context_chunks: List[Chunk]) -> str:
        context = "\n".join(chunk.content for chunk in context_chunks)

        return f"Query: {query}\n\nContext:\n{context}"