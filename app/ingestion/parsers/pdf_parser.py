import fitz

from app.ingestion.parsers.base import BaseParser


class PDFParser(BaseParser):

    def extract_text(self, file_bytes: bytes) -> str:
        document = fitz.open(stream=file_bytes, filetype="pdf")

        pages = []

        for page in document:
            pages.append(page.get_text())

        document.close()

        return "\n".join(pages)