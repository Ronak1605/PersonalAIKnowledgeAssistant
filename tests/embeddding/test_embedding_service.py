from embedding.embedding_service import EmbeddingService
from embedding.simple_embedder import SimpleEmbedder
from ingestion.models.chunk import Chunk


def test_embedding_service(tmp_path):
    embedder = SimpleEmbedder()
    service = EmbeddingService(embedder)

    chunks = [
        Chunk(id="1", input_id="1", content="hello", metadata={}, created_at=None),
        Chunk(id="2", input_id="1", content="world", metadata={}, created_at=None),
    ]

    vectors = service.embed_chunks(chunks)

    assert len(vectors) == 2