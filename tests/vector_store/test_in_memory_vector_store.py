from vector_store.in_memory_vector_store import InMemoryVectorStore
from ingestion.models.chunk import Chunk


def test_add_and_search():
    store = InMemoryVectorStore()

    chunks = [
        Chunk(id="1", input_id="1", content="hello world", metadata={}, created_at=None),
        Chunk(id="2", input_id="1", content="goodbye world", metadata={}, created_at=None),
    ]

    vectors = [
        [1.0, 2.0],
        [2.0, 1.0],
    ]

    store.add(vectors, chunks)

    query_vector = [1.0, 2.0]

    results = store.search(query_vector, top_k=1)

    assert len(results) == 1
    assert results[0][0].content == "hello world"


def test_top_k_limit():
    store = InMemoryVectorStore()

    chunks = [
        Chunk(id=str(i), input_id="1", content=f"text {i}", metadata={}, created_at=None)
        for i in range(5)
    ]

    vectors = [[float(i), float(i)] for i in range(5)]

    store.add(vectors, chunks)

    results = store.search([1.0, 1.0], top_k=2)

    assert len(results) == 2


def test_add_mismatched_lengths():
    store = InMemoryVectorStore()

    chunks = [Chunk(id="1", input_id="1", content="test", metadata={}, created_at=None)]
    vectors = []

    try:
        store.add(vectors, chunks)
        assert False
    except ValueError:
        assert True