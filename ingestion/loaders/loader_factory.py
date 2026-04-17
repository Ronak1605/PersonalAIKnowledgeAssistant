from ingestion.loaders.text_loader import TextLoader
from ingestion.loaders.pdf_loader import PDFLoader
from ingestion.loaders.email_loader import EmailLoader


class LoaderFactory:
    @staticmethod
    def get_loader(source: str):
        source = source.lower()

        if source.endswith(".txt"):
            return TextLoader()
        elif source.endswith(".md"):
            return TextLoader()
        elif source.endswith(".pdf"):
            return PDFLoader()
        elif source.endswith(".eml"):
            return EmailLoader()
        else:
            raise ValueError(f"Unsupported file type: {source}")