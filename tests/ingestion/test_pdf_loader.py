import hashlib
from pathlib import Path

import pytest
from reportlab.pdfgen import canvas

from ingestion.loaders.pdf_loader import PDFLoader
from ingestion.models.input_source import InputSource


def create_test_pdf(file_path: Path, pages: list[str]) -> None:
    """
    Utility function to create a multi-page PDF for testing.
    """
    c = canvas.Canvas(str(file_path))

    for page_text in pages:
        c.drawString(100, 750, page_text)
        c.showPage()

    c.save()


def test_pdf_loader_loads_pages(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    pages = ["First page", "Second page"]

    create_test_pdf(pdf_path, pages)

    loader = PDFLoader()
    inputs = loader.load(str(pdf_path))

    assert len(inputs) == 2

    for i, input_obj in enumerate(inputs, start=1):
        assert input_obj.source == InputSource.PDF
        assert pages[i - 1] in input_obj.content
        assert input_obj.metadata["page"] == str(i)
        assert input_obj.metadata["total_pages"] == "2"
        assert input_obj.metadata["file_name"] == "test.pdf"


def test_pdf_loader_deterministic_id(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    create_test_pdf(pdf_path, ["Only page"])

    loader = PDFLoader()

    inputs_first = loader.load(str(pdf_path))
    inputs_second = loader.load(str(pdf_path))

    assert inputs_first[0].id == inputs_second[0].id


def test_pdf_loader_file_not_found():
    loader = PDFLoader()

    with pytest.raises(FileNotFoundError):
        loader.load("non_existent.pdf")


def test_pdf_loader_invalid_file_type(tmp_path):
    txt_path = tmp_path / "test.txt"
    txt_path.write_text("Not a PDF")

    loader = PDFLoader()

    with pytest.raises(ValueError):
        loader.load(str(txt_path))