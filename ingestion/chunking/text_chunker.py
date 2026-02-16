import uuid
from datetime import datetime
from typing import List

from ingestion.models.input import Input
from ingestion.models.chunk import Chunk


class TextChunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, input_obj: Input) -> List[Chunk]:
        text = input_obj.content
        chunks = []

        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]

            chunk = Chunk(
                id=str(uuid.uuid4()),
                input_id=input_obj.id,
                content=chunk_text,
                created_at=datetime.now(),
                metadata={
                    **input_obj.metadata,
                    "chunk_start": str(start),
                    "chunk_end": str(end),
                },
            )

            chunks.append(chunk)

            start += self.chunk_size - self.overlap

        return chunks
