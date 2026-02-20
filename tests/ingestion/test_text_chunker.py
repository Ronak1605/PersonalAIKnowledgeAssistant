import uuid
import pytest

from ingestion.chunking.text_chunker import TextChunker
from ingestion.models.input import Input
from ingestion.models.input_source import InputSource


#------------------------
# Fixtures (repeated setup code)
# ------------------------

@pytest.fixture
def base_input():
    return Input(
        id="input-123",
        content="abcdefghij",
        source=InputSource.TEXT,
        metadata={"source": "unit-test"},
        created_at=None,
    )


# ------------------------
# Constructor validation
# ------------------------

def test_chunk_size_must_be_positive():
    with pytest.raises(ValueError):
        TextChunker(chunk_size=0)


def test_overlap_cannot_be_negative():
    with pytest.raises(ValueError):
        TextChunker(chunk_size=10, overlap=-1)


def test_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(ValueError):
        TextChunker(chunk_size=10, overlap=10)


# ------------------------
# Happy path tests
# ------------------------

def test_returns_list_of_chunks(base_input):
    chunker = TextChunker(chunk_size=5, overlap=0)

    chunks = chunker.chunk(base_input)

    assert isinstance(chunks, list)
    assert len(chunks) == 2


def test_correct_chunk_content(base_input):
    chunker = TextChunker(chunk_size=5, overlap=0)

    chunks = chunker.chunk(base_input)

    assert [c.content for c in chunks] == ["abcde", "fghij"]


def test_input_id_is_propagated(base_input):
    chunker = TextChunker(chunk_size=5, overlap=0)

    chunks = chunker.chunk(base_input)

    assert all(chunk.input_id == "input-123" for chunk in chunks)
    
# Metadata tests

def test_metadata_is_propagated(base_input):
    chunker = TextChunker(chunk_size=5, overlap=0)

    chunks = chunker.chunk(base_input)

    for chunk in chunks:
        assert chunk.metadata["source"] == "unit-test"


def test_chunk_position_metadata(base_input):
    chunker = TextChunker(chunk_size=5, overlap=0)

    chunks = chunker.chunk(base_input)

    assert chunks[0].metadata["chunk_start"] == "0"
    assert chunks[0].metadata["chunk_end"] == "5"

    assert chunks[1].metadata["chunk_start"] == "5"
    assert chunks[1].metadata["chunk_end"] == "10"

# Overlap behaviour

def test_overlap_behavior():
    chunker = TextChunker(chunk_size=5, overlap=2)

    input_obj = Input(
        id="input-1",
        content="abcdefghij",
        source=InputSource.TEXT,
        metadata={},
        created_at=None,
    )

    chunks = chunker.chunk(input_obj)

    assert [c.content for c in chunks] == [
        # Partial chunks at the end of the text are allowed, following most RAG implementations
        "abcde",
        "defgh",
        "ghij",
        "j"
    ]

# UUID & Timestamp integrity

def test_chunk_ids_are_valid_uuid(base_input):
    chunker = TextChunker(chunk_size=5, overlap=0)

    chunks = chunker.chunk(base_input)

    for chunk in chunks:
        uuid.UUID(chunk.id)  # Raises ValueError if invalid


def test_created_at_is_set(base_input):
    chunker = TextChunker(chunk_size=5, overlap=0)

    chunks = chunker.chunk(base_input)

    assert all(chunk.created_at is not None for chunk in chunks)


# ------------------------
# Edge cases
# ------------------------

def test_empty_content_returns_empty_list():
    chunker = TextChunker(chunk_size=5, overlap=0)

    input_obj = Input(
        id="input-1",
        content="",
        source=InputSource.TEXT,
        metadata={},
        created_at=None,
    )

    chunks = chunker.chunk(input_obj)

    assert chunks == []
