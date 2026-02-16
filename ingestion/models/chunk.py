from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class Chunk:
    id: str
    input_id: str
    content: str
    created_at: datetime
    metadata: Dict[str, str]