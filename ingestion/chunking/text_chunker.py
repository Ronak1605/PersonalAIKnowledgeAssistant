import uuid
from datetime import datetime, timezone
from typing import List

from ingestion.models.input import Input
from ingestion.models.chunk import Chunk


class TextChunker:
    """
    A simple text chunker that splits input text into chunks of a specified size with optional overlap.
    
    Args:
        chunk_size (int): The maximum size of each chunk. Default is 500 characters.
        overlap (int): The number of characters to overlap between chunks. Default is 50 characters.
        
    Raises:
        ValueError: If the overlap is greater than or equal to the chunk size.
    """
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if overlap < 0:
            raise ValueError("overlap cannot be negative")

        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, input_obj: Input) -> List[Chunk]:
        """
        Splits the input text into chunks based on the specified chunk size and overlap.
        
        Args:
            input_obj (Input): The input object containing the text to be chunked.
            
        Returns:
            List[Chunk]: A list of Chunk objects representing the chunked text.
        """
        
        text = input_obj.content or ""
        if not text:
            return []

        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]

            chunks.append(
                Chunk(
                    id=str(uuid.uuid4()),
                    input_id=input_obj.id,
                    content=chunk_text,
                    created_at=datetime.now(timezone.utc),
                    metadata={
                        **(input_obj.metadata or {}),
                        "chunk_start": str(start),
                        "chunk_end": str(min(end, len(text))),
                    },
                )
            )

            start += self.chunk_size - self.overlap

        return chunks
