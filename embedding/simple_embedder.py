from typing import List
from embedding.base_embedder import BaseEmbedder


class SimpleEmbedder(BaseEmbedder):
    """
    A simple placeholder embedder for testing.

    Converts text into deterministic numeric vectors.
    """

    def embed(self, texts: List[str]) -> List[List[float]]:
        embeddings = []

        for text in texts:
            # Simple deterministic embedding: character ord values (number representing the unicode code of a specified character)
            vector = [float(ord(c)) for c in text[:50]]  # truncate for consistency
            embeddings.append(vector)

        return embeddings