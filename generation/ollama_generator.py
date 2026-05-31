import requests
from typing import List

from ingestion.models.chunk import Chunk
from generation.base_generator import BaseGenerator


class OllamaGenerator(BaseGenerator):
    """
    Generator that uses a local Ollama model.
    """

    def __init__(self, model: str = "phi3:latest", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def generate(self, query: str, context_chunks: List[Chunk]) -> str:
        context = "\n\n".join(chunk.content for chunk in context_chunks)

        prompt = f"""
You are a helpful assistant. Use ONLY the provided context to answer the question.

If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{query}

Answer:
"""

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=60,
        )

        response.raise_for_status()

        return response.json()["response"]