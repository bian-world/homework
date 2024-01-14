from typing import Optional

from backend.ai_translator.book import Book
from backend.ai_translator.model import Model
from backend.ai_translator.translator.pdf_parser import PDFParser
from backend.ai_translator.translator.writer import Writer
from backend.ai_translator.utils import LOG


class PDFTranslator:
    def __init__(self, model: Model):
        self.model = model
        self.pdf_parser = PDFParser()
        self.writer = Writer()

    def translate_pdf(self, book: Book, file_format: str = 'PDF', target_language: str = '中文',
                      output_file_path: str = None, pages: Optional[int] = None):
        # self.book = self.pdf_parser.parse_pdf(pdf_file_path, pages)

        for page_idx, page in enumerate(book.pages):
            for content_idx, content in enumerate(page.contents):
                prompt = self.model.translate_prompt(content, target_language)
                LOG.debug(prompt)
                translation, status = self.model.make_request(prompt)
                # translation, status = 'result', True
                LOG.info(translation)

                # Update the content in self.book.pages directly
                book.pages[page_idx].contents[content_idx].set_translation(translation, status)

        return self.writer.save_translated_book(book, output_file_path, file_format)
