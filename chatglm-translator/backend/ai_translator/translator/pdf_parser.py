import pdfplumber
from typing import Optional

from werkzeug.datastructures import FileStorage

from backend.ai_translator import RESULT_FILE_DIR
from backend.ai_translator.book import Book, Content, ContentType, TableContent, Page
from backend.ai_translator.book.content import ImageContent
from backend.ai_translator.translator.exceptions import PageOutOfRangeException
from backend.ai_translator.utils import LOG


class PDFParser:
    def __init__(self):
        pass

    def parse_pdf(self, file: str, pages: Optional[int] = None) -> Book:
        book = None
        if type(file) == FileStorage:
            book = Book(RESULT_FILE_DIR + "/" + file.filename)
        else:
            book = Book(file)

        with pdfplumber.open(file) as pdf:
            if pages is not None and pages > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages), pages)

            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages]

            for pdf_page in pages_to_parse:
                page = Page()

                # Store the original text content
                raw_text = pdf_page.extract_text()
                tables = pdf_page.extract_tables()
                images = pdf_page.images

                # Remove each cell's content from the original text
                for table_data in tables:
                    for row in table_data:
                        for cell in row:
                            raw_text = raw_text.replace(cell, "", 1)

                # Handling text
                if raw_text:
                    # Remove empty lines and leading/trailing whitespaces
                    raw_text_lines = raw_text.splitlines()
                    cleaned_raw_text_lines = [line.strip() for line in raw_text_lines if line.strip()]
                    cleaned_raw_text = "\n".join(cleaned_raw_text_lines)

                    text_content = Content(content_type=ContentType.TEXT, original=cleaned_raw_text)
                    page.add_content(text_content)
                    LOG.debug(f"[raw_text]\n {cleaned_raw_text}")

                # Handling tables
                if tables:
                    table = TableContent(tables)
                    page.add_content(table)
                    LOG.debug(f"[table]\n{table}")

                if images:
                    for img in images:
                        bbox = (img["x0"], img["top"], img["x1"], img["bottom"])
                        image_content = ImageContent(pdf_page.crop(bbox).to_image(antialias=True))
                        page.add_content(image_content)

                book.add_page(page)

        return book
