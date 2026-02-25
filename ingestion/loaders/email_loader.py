from pathlib import Path
from typing import List
from datetime import datetime
import hashlib
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime

from ingestion.loaders.base import BaseLoader
from ingestion.models.input import Input
from ingestion.models.input_source import InputSource


class EmailLoader(BaseLoader):
    """
    Loader for extracting content from .eml email files.

    Returns one Input per email.
    """

    def load(self, source: str) -> List[Input]:
        file_path = Path(source)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix.lower() != ".eml":
            raise ValueError(f"Invalid file type: {file_path.suffix}")

        with open(file_path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)

        subject = msg.get("subject", "")
        sender = msg.get("from", "")
        recipient = msg.get("to", "")
        message_id = msg.get("message-id", "")

        # Extract body
        body = self._extract_body(msg)

        # Determine created_at
        date_header = msg.get("date")
        created_at = None
        if date_header:
            try:
                created_at = parsedate_to_datetime(date_header)
            except Exception:
                created_at = None

        # Deterministic ID
        unique_string = message_id or f"{file_path.resolve()}::{body}"
        input_id = hashlib.sha256(unique_string.encode()).hexdigest()

        input_obj = Input(
            id=input_id,
            content=body,
            source=InputSource.EMAIL,
            created_at=created_at,
            metadata={
                "subject": subject,
                "from": sender,
                "to": recipient,
                "message_id": message_id,
                "file_name": file_path.name,
                "file_path": str(file_path.resolve()),
            },
        )

        return [input_obj]

    def _extract_body(self, msg) -> str:
        """
        Extracts the best available body content from an email message.
        Prefers text/plain over text/html.
        """

        if msg.is_multipart():
            # Prefer text/plain
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    return part.get_content().strip()

            # Fallback to text/html
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/html":
                    return part.get_content().strip()

            return ""
        else:
            return msg.get_content().strip()