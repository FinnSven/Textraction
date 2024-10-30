import sys

import ebooklib
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QFileDialog
from ebooklib import epub
from bs4 import BeautifulSoup
import os


class EpubExtractor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EPUB to Text Extractor")
        self.setGeometry(100, 100, 400, 200)

        # Create layout and widgets
        layout = QVBoxLayout()

        # Source file label and textbox
        self.source_label = QLabel("Select EPUB File:")
        layout.addWidget(self.source_label)

        self.source_textbox = QLineEdit(self)
        layout.addWidget(self.source_textbox)

        self.source_button = QPushButton("Browse")
        self.source_button.clicked.connect(self.browse_source)
        layout.addWidget(self.source_button)

        # Output folder label and textbox
        self.output_label = QLabel("Select Output Folder:")
        layout.addWidget(self.output_label)

        self.output_textbox = QLineEdit(self)
        layout.addWidget(self.output_textbox)

        self.output_button = QPushButton("Browse")
        self.output_button.clicked.connect(self.browse_output)
        layout.addWidget(self.output_button)

        # Extract button
        self.extract_button = QPushButton("Extract Text")
        self.extract_button.clicked.connect(self.extract_text_from_epub)
        layout.addWidget(self.extract_button)

        # Set main widget and layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_source(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select EPUB File", "", "EPUB Files (*.epub);;All Files (*)",
                                                   options=options)
        if file_name:
            self.source_textbox.setText(file_name)

    def browse_output(self):
        options = QFileDialog.Options()
        folder_name = QFileDialog.getExistingDirectory(self, "Select Output Folder", options=options)
        if folder_name:
            self.output_textbox.setText(folder_name)

    def extract_text_from_epub(self):
        source_path = self.source_textbox.text()
        output_folder = self.output_textbox.text()

        if not source_path or not output_folder:
            print("Please select both a source file and an output folder.")
            return

        try:
            book = epub.read_epub(source_path)
            text_content = []

            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_body_content(), 'html.parser')
                    text_content.append(soup.get_text())

            output_file_path = os.path.join(output_folder, os.path.splitext(os.path.basename(source_path))[0] + '.txt')

            with open(output_file_path, 'w', encoding='utf-8') as fout:
                fout.write('\n'.join(text_content))

            print(f"Text extracted and saved to {output_file_path}")

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EpubExtractor()
    window.show()
    sys.exit(app.exec_())
