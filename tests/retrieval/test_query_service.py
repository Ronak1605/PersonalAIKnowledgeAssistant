from retrieval.query_service import QueryService
from embedding.simple_embedder import SimpleEmbedder
from vector_store.in_memory_vector_store import InMemoryVectorStore
from ingestion.models.chunk import Chunk


def test_query_returns_relevant_chunks():
    embedder = SimpleEmbedder()
    store = InMemoryVectorStore()

    chunks = [
        Chunk(id="1", input_id="1", content="hello world", metadata={}, created_at=None),
        Chunk(id="2", input_id="1", content="goodbye world", metadata={}, created_at=None),
    ]

    vectors = embedder.embed([c.content for c in chunks])
    store.add(vectors, chunks)

    service = QueryService(embedder, store)

    results = service.query("hello", top_k=1)

    assert len(results) == 1
    assert "hello" in results[0][0].content