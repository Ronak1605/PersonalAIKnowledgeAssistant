from typing import List, Tuple
import math

from vector_store.base_vector_store import BaseVectorStore
from ingestion.models.chunk import Chunk


class InMemoryVectorStore(BaseVectorStore):
    """
    Simple in-memory vector store using cosine similarity.
    """

    def __init__(self):
        self.vectors: List[List[float]] = []
        self.chunks: List[Chunk] = []

    def add(self, vectors: List[List[float]], chunks: List[Chunk]) -> None:
        if len(vectors) != len(chunks):
            raise ValueError("Vectors and chunks must have same length")

        self.vectors.extend(vectors)
        self.chunks.extend(chunks)

    def search(self, query_vector: List[float], top_k: int) -> List[Tuple[Chunk, float]]:
        results = []

        for vector, chunk in zip(self.vectors, self.chunks):
            score = self._cosine_similarity(query_vector, vector)
            results.append((chunk, score))

        # Sort by similarity (descending)
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:top_k]

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        # Handle different lengths (due to simple embedder)
        min_len = min(len(v1), len(v2))
        v1 = v1[:min_len]
        v2 = v2[:min_len]

        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot / (norm1 * norm2)