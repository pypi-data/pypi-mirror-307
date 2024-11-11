from typing import List

from bs4 import BeautifulSoup

import ebook2text.ebooklib as ebooklib
from ebook2text.ebooklib import epub

from ._types import EpubBook, EpubItem, ResultSet, Tag
from .abstract_book import (
    BookConversion,
    ChapterSplit,
    ImageExtraction,
    TextExtraction,
)
from .chapter_check import NOT_CHAPTER, is_chapter, is_not_chapter
from .ocr import encode_image_file, run_ocr


class EpubConverter(BookConversion):
    """
    Converts EPUB files to text and splits chapters.

    This class extends the BookConversion abstract class and provides methods
    for reading EPUB files,extracting text from elements, extracting images,
    processing chapter text, and splitting chapters.

    Args:
        file_path (str): The path to the EPUB file to be read.
        metadata (dict): A dictionary containing metadata such as title and
            author information.
    """

    def _read_file(self, file_path: str) -> EpubBook:
        """Reads Epub file using Ebooklib package"""
        return epub.read_epub(file_path, options={"ignore_ncx": True})

    def extract_images(self, element: Tag) -> List[str]:
        """Delegates to EpubImageExtractor to extract images."""
        image_extractor = EpubImageExtractor(self.book)
        return image_extractor.extract_images(element)

    def extract_text(self, element: Tag) -> str:
        """Delegates to EpubTextExtractor to extract text."""
        text_extractor = EpubTextExtractor(self)
        return text_extractor.extract_text(element)

    def split_chapters(self) -> str:
        """
        Splits the EPUB file into chapters.
        """
        splitter = EpubChapterSplitter(self.book, self.metadata, self)
        return splitter.split_chapters()


class EpubTextExtractor(TextExtraction):
    """
    Extracts text from EPUB elements, handling image OCR.
    """

    def __init__(self, converter: EpubConverter):
        self.converter = converter

    def extract_text(self, element: Tag) -> str:
        """
        Extracts text from an element, using OCR for images.

        Args:
            element: The element from which text needs to be extracted.
            book (EpubBook): The EpubBook object for accessing image data.

        Returns:
            str: The extracted text from the element.
        """
        if element.name == "img":
            return self._extract_image_text(element)
        else:
            return self._extract_text(element)

    def _extract_image_text(self, element: Tag) -> str:
        base64_images: list = self.converter.extract_images(element)
        return run_ocr(base64_images)

    def _extract_text(self, element: Tag) -> str:
        return element.get_text().strip()


class EpubImageExtractor(ImageExtraction):
    """
    Extracts images from an EPUB file.
    """

    def __init__(self, book: EpubBook):
        self.book = book

    def extract_images(self, element: Tag) -> list:
        """
        Extracts images from the EPUB file.

        Args:
            element: The element containing the image data.

        Returns:
            list: A list of encoded image data.
        """
        image_data: EpubItem = self.book.get_item_with_href(element["src"])
        return [encode_image_file(image_data)]


class EpubChapterSplitter(ChapterSplit[EpubBook]):
    """
    Splits an EPUB file into chapters.
    """

    def __init__(
        self, book: EpubBook, metadata: dict, converter: EpubConverter
    ) -> None:
        super().__init__(book, metadata, converter)
        self.book = self.text_obj

    def _process_chapter_text(self, item) -> str:
        """
        Extracts text from a chapter item.

        Args:
            item: ebooklib item representing a chapter.

        Returns:
            str: String containing the text of the chapter.
        """
        TEXT_ELEMENTS = ["p", "img", "h1", "h2", "h3", "h4", "h5", "h6"]
        soup = BeautifulSoup(item.content, "html.parser")
        elements: ResultSet[Tag] = soup.find_all(TEXT_ELEMENTS)

        for i, element in enumerate(elements[: self.MAX_LINES_TO_CHECK]):
            text = self.converter.extract_text(element)
            if any(word in NOT_CHAPTER for word in text.split()):
                return ""
            elif is_chapter(text):
                starting_line = i + 1
                return "\n".join(
                    tag.get_text().strip()
                    for tag in elements[starting_line:]
                    if tag != "img"
                )
        return ""

    def split_chapters(self) -> str:
        """
        Split the EPUB file into chapters and return the cleaned text.

        Returns:
            str: The cleaned text of the chapters separated by '***'.
        """
        chapters: list = []
        join_char = f"\n{self.CHAPTER_SEPARATOR}\n"
        for item in self.book.get_items():
            if (
                item.get_type() == ebooklib.ITEM_DOCUMENT
                and not is_not_chapter(item.file_name.lower(), self.metadata)
            ):
                if chapter_text := self._process_chapter_text(item):
                    chapters.append(self.clean_text(chapter_text))
        return join_char.join(chapters)


def read_epub(file_path: str, metadata: dict) -> str:
    """
    Reads an EPUB file and splits it into chapters.

    Args:
        file_path (str): The path to the EPUB file to be read.
        metadata (dict): A dictionary containing metadata such as title and
            author information.

    Returns:
        str: The cleaned text of the chapters separated by '***'.
    """
    epub_converter = EpubConverter(file_path, metadata)
    return epub_converter.split_chapters()
