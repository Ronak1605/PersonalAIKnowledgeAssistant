from typing import List, Tuple

from embedding.base_embedder import BaseEmbedder
from vector_store.base_vector_store import BaseVectorStore
from ingestion.models.chunk import Chunk


class QueryService:
    """
    Handles querying over the vector store.
    """

    def __init__(self, embedder: BaseEmbedder, vector_store: BaseVectorStore):
        self.embedder = embedder
        self.vector_store = vector_store

    def query(self, text: str, top_k: int = 3) -> List[Tuple[Chunk, float]]:
        # Embed query
        query_vector = self.embedder.embed([text])[0]

        # Search vector store
        results = self.vector_store.search(query_vector, top_k)

        return results