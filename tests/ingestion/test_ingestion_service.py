from ingestion.ingestion_service import IngestionService
from ingestion.chunking.text_chunker import TextChunker


def test_ingestion_pipeline_text(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello world " * 50)

    service = IngestionService(chunker=TextChunker(chunk_size=50, overlap=0))

    chunks = service.ingest(str(file_path))

    assert len(chunks) > 1
    assert all(chunk.content for chunk in chunks)