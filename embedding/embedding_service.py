from typing import List

from embedding.base_embedder import BaseEmbedder
from ingestion.models.chunk import Chunk


class EmbeddingService:
    """
    Handles embedding generation for chunks.
    """

    def __init__(self, embedder: BaseEmbedder):
        self.embedder = embedder

    def embed_chunks(self, chunks: List[Chunk]) -> List[List[float]]:
        texts = [chunk.content for chunk in chunks]
        return self.embedder.embed(texts)