import pytest
from pathlib import Path
from email.message import EmailMessage
from datetime import datetime

from ingestion.loaders.email_loader import EmailLoader
from ingestion.models.input import InputSource

# -------------------------
# Helper functions
# -------------------------

def create_eml_file(
    path: Path,
    subject: str = "Test Email",
    body: str = "Hello world",
    from_addr: str = "sender@example.com",
    to_addr: str = "recipient@example.com",
    message_id: str = "<1234@test>",
    date: str = "Mon, 01 Jan 2024 10:00:00 +0000",
):
    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg["Message-ID"] = message_id
    msg["Date"] = date
    msg.set_content(body)

    with open(path, "wb") as f:
        f.write(msg.as_bytes())


# -------------------------
# Metadata tests
# -------------------------

def test_email_loader_simple_plain_text(tmp_path):
    eml_path = tmp_path / "test.eml"

    create_eml_file(
        eml_path,
        subject="Test Email",
        body="Hello this is a test email.",
    )

    loader = EmailLoader()
    inputs = loader.load(str(eml_path))

    assert len(inputs) == 1

    input_obj = inputs[0]

    assert input_obj.source == InputSource.EMAIL
    assert input_obj.metadata["subject"] == "Test Email"
    assert input_obj.metadata["from"] == "sender@example.com"
    assert input_obj.metadata["to"] == "recipient@example.com"
    assert input_obj.metadata["message_id"] == "<1234@test>"

    assert "Hello this is a test email." in input_obj.content

# -----------------------------
# Edge cases and special cases
# -----------------------------


def test_email_loader_empty_body(tmp_path):
    eml_path = tmp_path / "empty.eml"

    create_eml_file(
        eml_path,
        subject="Empty Body",
        body="",
    )

    loader = EmailLoader()
    inputs = loader.load(str(eml_path))

    assert len(inputs) == 1
    assert inputs[0].content.strip() == ""


def test_email_loader_missing_subject(tmp_path):
    eml_path = tmp_path / "no_subject.eml"

    msg = EmailMessage()
    msg["From"] = "sender@example.com"
    msg["To"] = "recipient@example.com"
    msg["Date"] = "Mon, 01 Jan 2024 10:00:00 +0000"
    msg.set_content("No subject here.")

    with open(eml_path, "wb") as f:
        f.write(msg.as_bytes())

    loader = EmailLoader()
    inputs = loader.load(str(eml_path))

    assert len(inputs) == 1
    assert inputs[0].metadata.get("subject", "") == ""


def test_email_loader_multipart_plain_and_html(tmp_path):
    eml_path = tmp_path / "multipart.eml"

    msg = EmailMessage()
    msg["From"] = "sender@example.com"
    msg["To"] = "recipient@example.com"
    msg["Subject"] = "Multipart Email"
    msg["Date"] = "Mon, 01 Jan 2024 10:00:00 +0000"

    msg.set_content("This is the plain text version.")
    msg.add_alternative(
        "<html><body><p>This is the HTML version.</p></body></html>",
        subtype="html",
    )

    with open(eml_path, "wb") as f:
        f.write(msg.as_bytes())

    loader = EmailLoader()
    inputs = loader.load(str(eml_path))

    assert len(inputs) == 1

    content = inputs[0].content

    # Loader should prefer plain text over HTML
    assert "This is the plain text version." in content