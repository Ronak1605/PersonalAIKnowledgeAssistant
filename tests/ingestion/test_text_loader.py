import pytest

from ingestion.loaders.text_loader import TextLoader
from ingestion.models.input_source import InputSource

# ------------------------
# Fixtures (repeated setup code)
# ------------------------

@pytest.fixture
def loader():
    return TextLoader()

# ------------------------
# Helper functions
# ------------------------

def get_single_input(results):
    assert len(results) == 1
    return results[0]


# ------------------------
# Happy path tests
# ------------------------

def test_reads_basic_text_file(tmp_path, loader):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello world")

    results = loader.load(file_path)
    input_obj = get_single_input(results)

    assert input_obj.content == "Hello world"
    assert input_obj.source == InputSource.TEXT


# ------------------------
# Edge cases & special cases
# ------------------------

def test_handles_empty_file(tmp_path, loader):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("")

    results = loader.load(file_path)
    input_obj = get_single_input(results)

    assert input_obj.content == ""
    assert input_obj.source == InputSource.TEXT


def test_preserves_unicode_characters(tmp_path, loader):
    content = "Hello 🌍 — café naïve 中文 عربى"
    file_path = tmp_path / "unicode.txt"
    file_path.write_text(content, encoding="utf-8")

    results = loader.load(file_path)
    input_obj = get_single_input(results)

    assert input_obj.content == content
    assert input_obj.source == InputSource.TEXT


def test_preserves_whitespace(tmp_path, loader):
    content = "  Hello world\n\n"
    file_path = tmp_path / "whitespace.txt"
    file_path.write_text(content)

    results = loader.load(file_path)
    input_obj = get_single_input(results)

    assert input_obj.content == content
    assert input_obj.source == InputSource.TEXT


# ------------------------
# Error handling
# ------------------------

def test_raises_error_when_file_does_not_exist(loader):
    with pytest.raises(FileNotFoundError):
        loader.load("does_not_exist.txt")