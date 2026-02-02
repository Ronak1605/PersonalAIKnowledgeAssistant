from enum import Enum

class InputSource(str, Enum):
    """
    Enumerates supported input types.
    """
    TEXT = "text"
    MARKDOWN = "markdown"
    PDF = "pdf"
    EMAIL = "email"
