import time

from ingestion.ingestion_service import IngestionService
from ingestion.chunking.text_chunker import TextChunker

from embedding.simple_embedder import SimpleEmbedder
from embedding.embedding_service import EmbeddingService

from vector_store.in_memory_vector_store import InMemoryVectorStore

from retrieval.query_service import QueryService

from generation.ollama_generator import OllamaGenerator

from rag.rag_service import RAGService


# ------------------------
# Setup pipeline components
# ------------------------

chunker = TextChunker(chunk_size=500, overlap=50)

ingestion_service = IngestionService(chunker)

embedder = SimpleEmbedder()

embedding_service = EmbeddingService(embedder)

vector_store = InMemoryVectorStore()

query_service = QueryService(embedder, vector_store)

generator = OllamaGenerator(model="phi3:latest")

rag_service = RAGService(query_service, generator)


# ------------------------
# Ingest a file
# ------------------------

chunks = ingestion_service.ingest("example_data/example.txt")

vectors = embedding_service.embed_chunks(chunks)

vector_store.add(vectors, chunks)


# ------------------------
# Query loop
# ------------------------

while True:
    query = input("\nAsk a question (or 'quit'): ")

    if query.lower() == "quit":
        break

    start = time.time()

    answer = rag_service.ask(query)

    print(f"\nResponse generated in {time.time() - start:.2f} seconds")

    print("\nAnswer:")
    print(answer)