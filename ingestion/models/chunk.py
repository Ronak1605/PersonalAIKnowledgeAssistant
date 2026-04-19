from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


@dataclass
class Chunk:
    id: str
    input_id: str
    content: str
    created_at: Optional[datetime]
    metadata: Dict[str, str]