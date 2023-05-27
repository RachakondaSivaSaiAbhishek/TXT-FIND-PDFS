import os
import re
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QMessageBox, QListWidget, QAbstractItemView
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from PyPDF2 import PdfReader


class PdfSearchViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" TXTFINDER ")
        self.setGeometry(100, 100, 500, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f2f2f2;
            }
            QLabel {
                font: 10pt "Helvetica";
            }
            QPushButton {
                font: 10pt "Helvetica";
                background-color: #4CAF50;
                color: white;
                padding: 6px 10px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                font: 10pt "Helvetica";
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QListWidget {
                font: 10pt "Helvetica";
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px;
            }
        """)

        self.setWindowIcon(QIcon("C:/Users/Abhishek/Desktop/pdf/image.png"))

        self.setup_ui()

    def setup_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layouts
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Folder Path
        folder_layout = QHBoxLayout()
        folder_label = QLabel("Folder Path:")
        self.folder_path_entry = QLineEdit()
        self.folder_path_entry.setPlaceholderText("Select a folder...")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_folder_callback)

        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_path_entry)
        folder_layout.addWidget(browse_button)

        # Keyword Entry
        keyword_layout = QVBoxLayout()
        mandatory_keywords_label = QLabel("Mandatory Keywords (comma-separated):")
        self.mandatory_keywords_entry = QLineEdit()
        optional_keywords_label = QLabel("Optional Keywords (comma-separated):")
        self.optional_keywords_entry = QLineEdit()
        exclusion_keywords_label = QLabel("Exclusion Keywords (comma-separated):")
        self.exclusion_keywords_entry = QLineEdit()

        keyword_layout.addWidget(mandatory_keywords_label)
        keyword_layout.addWidget(self.mandatory_keywords_entry)
        keyword_layout.addWidget(optional_keywords_label)
        keyword_layout.addWidget(self.optional_keywords_entry)
        keyword_layout.addWidget(exclusion_keywords_label)
        keyword_layout.addWidget(self.exclusion_keywords_entry)

        # Search Button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_files_callback)

        # File List
        file_list_label = QLabel("Result Files:")
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.file_list.itemDoubleClicked.connect(self.open_pdf)

        # Add widgets to main layout
        main_layout.addLayout(folder_layout)
        main_layout.addLayout(keyword_layout)
        main_layout.addWidget(search_button)
        main_layout.addWidget(file_list_label)
        main_layout.addWidget(self.file_list)

        # Set alignment and margins for the main layout
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(20, 20, 20, 20)

    def browse_folder_callback(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.folder_path_entry.setText(folder_path)

    def search_files_callback(self):
        folder_path = self.folder_path_entry.text().strip()
        mandatory_keywords = [keyword.strip() for keyword in self.mandatory_keywords_entry.text().split(',')]
        optional_keywords = [keyword.strip() for keyword in self.optional_keywords_entry.text().split(',') if keyword.strip()]
        exclusion_keywords = [keyword.strip() for keyword in self.exclusion_keywords_entry.text().split(',') if keyword.strip()]

        if not folder_path or not mandatory_keywords:
            QMessageBox.critical(self, "Error", "Please provide a folder path and at least one mandatory keyword.")
            return

        if not os.path.isdir(folder_path):
            QMessageBox.critical(self, "Error", "Invalid folder path.")
            return

        found_files = self.search_pdf_files(folder_path, mandatory_keywords, optional_keywords, exclusion_keywords)
        if found_files:
            self.file_list.clear()
            self.file_list.addItems(found_files)
        else:
            QMessageBox.information(self, "Result", "No files found containing the specified keywords.")

    def search_pdf_files(self, folder_path, mandatory_keywords, optional_keywords, exclusion_keywords):
        pdf_files = []
        for file in os.listdir(folder_path):
            if file.endswith('.pdf'):
                pdf_files.append(file)
        sorted_files = sorted(pdf_files)

        found_files = []
        for file in sorted_files:
            pdf_path = os.path.join(folder_path, file)
            with open(pdf_path, 'rb') as f:
                pdf = PdfReader(f)
                for page in pdf.pages:
                    text = page.extract_text()
                    if all(re.search(r'\b{}\b'.format(keyword), text, re.IGNORECASE) for keyword in mandatory_keywords):
                        if not exclusion_keywords or not any(re.search(r'\b{}\b'.format(keyword), text, re.IGNORECASE) for keyword in exclusion_keywords):
                            if not optional_keywords or any(re.search(r'\b{}\b'.format(keyword), text, re.IGNORECASE) for keyword in optional_keywords):
                                found_files.append(file)
                                break

        return found_files

    def open_pdf(self, item):
        selected_file = item.text()
        folder_path = self.folder_path_entry.text().strip()
        pdf_path = os.path.join(folder_path, selected_file)
        os.startfile(pdf_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PdfSearchViewer()
    window.show()
    sys.exit(app.exec_())
