import uuid
from pathlib import Path
from datetime import datetime

from ingestion.loaders.base import BaseLoader
from ingestion.models.input import Input
from ingestion.models.input_source import InputSource


class TextLoader(BaseLoader):
    """
    Loader for plain text files.
    """

    def load(self, source: str):
        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {source}")

        if not path.is_file():
            raise ValueError(f"Input path is not a file: {source}")

        content = path.read_text(encoding="utf-8")

        return [
            Input(
                id=str(uuid.uuid4()),
                content=content,
                source=InputSource.TEXT,
                created_at=datetime.fromtimestamp(path.stat().st_mtime),
                metadata={
                    "filename": path.name,
                    "path": str(path),
                },
            )
        ]
