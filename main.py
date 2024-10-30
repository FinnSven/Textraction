import argparse

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os


def extract_text_from_epub(file_path, output_folder):
    try:
        # Load the EPUB book
        book = epub.read_epub(file_path)

        # Extract text from each document item in the book
        text = []
        for item in book.get_items():
            # Check if the item is an HTML document
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_body_content(), 'html.parser')
                text.append(soup.get_text())

        # Define output file path
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(file_path))[0] + '.txt')

        # Write the extracted text to a file
        with open(output_file, 'w', encoding='utf-8') as fout:
            fout.write('\n'.join(text))

        print(f"Text extracted and saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    parser = argparse.ArgumentParser(description='Extract text from an EPUB file and save it as a text file.')
    parser.add_argument('source', type=str, help='Path to the source EPUB file.')
    parser.add_argument('output_folder', type=str, help='Path to the folder where the text file will be saved.')

    args = parser.parse_args()

    extract_text_from_epub(args.source, args.output_folder)


if __name__ == "__main__":
    main()
