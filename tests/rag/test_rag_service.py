from rag.rag_service import RAGService
from retrieval.query_service import QueryService
from embedding.simple_embedder import SimpleEmbedder
from vector_store.in_memory_vector_store import InMemoryVectorStore
from generation.simple_generator import SimpleGenerator
from ingestion.models.chunk import Chunk


def test_rag_pipeline():
    embedder = SimpleEmbedder()
    store = InMemoryVectorStore()

    chunks = [
        Chunk(id="1", input_id="1", content="Python is a programming language", metadata={}, created_at=None),
        Chunk(id="2", input_id="1", content="Java is also a programming language", metadata={}, created_at=None),
    ]

    vectors = embedder.embed([c.content for c in chunks])
    store.add(vectors, chunks)

    query_service = QueryService(embedder, store)
    generator = SimpleGenerator()

    rag = RAGService(query_service, generator)

    answer = rag.ask("What is Python?")

    assert "Python" in answer