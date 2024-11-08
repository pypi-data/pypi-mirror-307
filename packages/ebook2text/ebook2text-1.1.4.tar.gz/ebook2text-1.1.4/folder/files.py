import os

from ebook2text.convert_file import convert_file


pdf_metadata = {
    "title": "Absolve",
    "author": "Edward Antrobus"
}
pdf_file = os.path.join("folder", "absolve.pdf")
epub_metadata = {
    "title": "Royal Dragon",
    "author": "Ash Roberts"
}
epub_file = os.path.join("folder", "royal.epub")


def main():
    convert_file(pdf_file, pdf_metadata)


if __name__ == "__main__":
    main()
