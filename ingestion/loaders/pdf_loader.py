from pathlib import Path
from typing import List
from datetime import datetime
import hashlib

from pypdf import PdfReader

from ingestion.loaders.base import BaseLoader
from ingestion.models.input import Input
from ingestion.models.input_source import InputSource


class PDFLoader(BaseLoader):
    """
    Loader for extracting text from a PDF file.

    Returns one Input per non-empty page.
    """

    def load(self, source: str) -> List[Input]:
        file_path = Path(source)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix.lower() != ".pdf":
            raise ValueError(f"Invalid file type: {file_path.suffix}")

        reader = PdfReader(str(file_path))
        total_pages = len(reader.pages)

        # Use the file's last modified time as the created_at timestamp for all pages
        created_at = datetime.fromtimestamp(file_path.stat().st_mtime)

        inputs: List[Input] = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            if not text.strip():
                continue

            unique_string = f"{file_path.resolve()}::page::{page_number}"
            input_id = hashlib.sha256(unique_string.encode()).hexdigest()

            inputs.append(
                Input(
                    id=input_id,
                    content=text,
                    source=InputSource.PDF,
                    created_at=created_at,
                    metadata={
                        "file_name": file_path.name,
                        "file_path": str(file_path.resolve()),
                        "page": str(page_number),
                        "total_pages": str(total_pages),
                    },
                )
            )

        return inputs