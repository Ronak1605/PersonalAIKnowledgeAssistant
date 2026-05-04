from abc import ABC, abstractmethod
from typing import List
from ingestion.models.chunk import Chunk


class BaseGenerator(ABC):
    @abstractmethod
    def generate(self, query: str, context_chunks: List[Chunk]) -> str:
        pass