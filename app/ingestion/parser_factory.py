from app.models.document import Document

from app.ingestion.parsers.pdf_parser import PDFParser
from app.ingestion.parsers.image_parser import ImageParser
# from app.ingestion.parsers.text_parser import TextParser
# from app.ingestion.parsers.html_parser import HTMLParser
# from app.ingestion.parsers.markdown_parser import MarkdownParser


class ParserFactory:

    PARSERS = {
        "application/pdf": PDFParser,
        "image/png": ImageParser,
        "image/jpeg": ImageParser,
        "image/webp": ImageParser,
        # "text/plain": TextParser,
        # "text/html": HTMLParser,
        # "text/markdown": MarkdownParser,
    }

    @staticmethod
    def get(document: Document):

        parser = ParserFactory.PARSERS.get(document.content_type)

        if parser is None:
            raise ValueError(
                f"Unsupported mime type: {document.content_type}"
            )

        return parser()