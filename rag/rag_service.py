from typing import List

from retrieval.query_service import QueryService
from generation.base_generator import BaseGenerator
from ingestion.models.chunk import Chunk


class RAGService:
    def __init__(self, query_service: QueryService, generator: BaseGenerator):
        self.query_service = query_service
        self.generator = generator

    def ask(self, query: str, top_k: int = 3) -> str:
        # Retrieve relevant chunks
        results = self.query_service.query(query, top_k)

        chunks: List[Chunk] = [chunk for chunk, _ in results]

        # Generate response
        return self.generator.generate(query, chunks)