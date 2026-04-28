from abc import ABC, abstractmethod
from typing import List, Tuple

from ingestion.models.chunk import Chunk


class BaseVectorStore(ABC):
    """
    Abstract interface for vector storage and retrieval.
    """

    @abstractmethod
    def add(self, vectors: List[List[float]], chunks: List[Chunk]) -> None:
        """
        Store vectors along with their associated chunks.
        """
        pass

    @abstractmethod
    def search(self, query_vector: List[float], top_k: int) -> List[Tuple[Chunk, float]]:
        """
        Return top_k most similar chunks with similarity scores.
        """
        pass