from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime
from ingestion.models.input_source import InputSource


@dataclass
class Input:
    """
    Representation for all ingested content.
    """
    id: str
    content: str
    source: InputSource
    created_at: Optional[datetime]
    metadata: Dict[str, str]
