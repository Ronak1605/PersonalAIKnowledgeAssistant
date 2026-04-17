from typing import List

from ingestion.loaders.loader_factory import LoaderFactory
from ingestion.chunking.text_chunker import TextChunker
from ingestion.models.chunk import Chunk
from ingestion.models.input import Input


class IngestionService:
    """
    Service for orchestrating the ingestion pipeline:
    source → loader → inputs → chunker → chunks
    """

    def __init__(self, chunker: TextChunker):
        self.chunker = chunker

    def ingest(self, source: str) -> List[Chunk]:
        # Select correct loader
        loader = LoaderFactory.get_loader(source)

        # Load inputs
        inputs: List[Input] = loader.load(source)

        # Chunk inputs
        chunks: List[Chunk] = []
        for input_obj in inputs:
            chunks.extend(self.chunker.chunk(input_obj))

        return chunks