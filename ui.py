from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QLineEdit, QPushButton, QRadioButton, QButtonGroup,
                            QLabel, QMessageBox)
import sys
import os
from datetime import datetime
from resume.generator import ResumeGenerator
from coverletter.generator import CoverLetterGenerator

class ResumeGeneratorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resume & Cover Letter Generator")
        self.setGeometry(100, 100, 600, 400)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Input fields
        self.company_name = QLineEdit()
        self.company_name.setPlaceholderText("Company Name")  # Fixed method name
        layout.addWidget(QLabel("Company Name:"))
        layout.addWidget(self.company_name)

        self.role_name = QLineEdit()
        self.role_name.setPlaceholderText("e.g. Software Engineer Intern")  # Fixed method name
        layout.addWidget(QLabel("Role Name:"))
        layout.addWidget(self.role_name)

        self.job_url = QLineEdit()
        self.job_url.setPlaceholderText("Job Description URL (optional)")  # Fixed method name
        layout.addWidget(QLabel("Job URL:"))
        layout.addWidget(self.job_url)

        # Document type selection
        layout.addWidget(QLabel("\nSelect document(s) to generate:"))
        self.btn_group = QButtonGroup()

        self.resume_only = QRadioButton("Resume Only")
        self.cover_only = QRadioButton("Cover Letter Only")
        self.both = QRadioButton("Both")
        self.both.setChecked(True)

        self.btn_group.addButton(self.resume_only)
        self.btn_group.addButton(self.cover_only)
        self.btn_group.addButton(self.both)

        layout.addWidget(self.resume_only)
        layout.addWidget(self.cover_only)
        layout.addWidget(self.both)

        # Generate button
        self.generate_btn = QPushButton("Generate Documents")
        self.generate_btn.clicked.connect(self.generate_documents)
        layout.addWidget(self.generate_btn)

        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

    def get_choice(self):
        if self.resume_only.isChecked():
            return "1"
        elif self.cover_only.isChecked():
            return "2"
        return "3"

    def create_output_structure(self, base_dir, company_name, role_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        date_dir = datetime.now().strftime("%Y%m%d")

        structure = {
            'company': company_name.lower().replace(' ', '_'),
            'role': role_name.lower().replace(' ', '_'),
            'date': date_dir,
            'timestamp': timestamp
        }

        output_path = os.path.join(
            base_dir,
            "applications",
            structure['company'],
            structure['role'],
            structure['date'],
            structure['timestamp']
        )

        os.makedirs(output_path, exist_ok=True)
        return output_path

    def generate_documents(self):
        try:
            company_name = self.company_name.text().strip()
            role_name = self.role_name.text().strip()
            job_url = self.job_url.text().strip()

            if not company_name or not role_name:
                QMessageBox.warning(self, "Input Error",
                                  "Company name and role name are required!")
                return

            base_dir = os.getcwd()
            output_dir = self.create_output_structure(base_dir, company_name, role_name)

            # Save job description if provided
            if job_url:
                with open(os.path.join(output_dir, 'job_description.txt'), 'w') as f:
                    f.write(f"URL: {job_url}\n\n")

            choice = self.get_choice()
            generated_files = []

            # Generate documents based on choice
            if choice in ['1', '3']:
                resume_file = os.path.join(output_dir, 'resume.pdf')
                resume_generator = ResumeGenerator(os.path.join(base_dir, "resume", "resume.yml"))
                output_file = resume_generator.generate_pdf(resume_file, output_dir)
                generated_files.append(output_file)

            if choice in ['2', '3']:
                cover_letter_file = os.path.join(output_dir, 'cover_letter.pdf')
                coverletter_generator = CoverLetterGenerator(
                    os.path.join(base_dir, "coverletter", "coverletter.yml"))
                output_file = coverletter_generator.generate_pdf(
                    cover_letter_file, output_dir, company_name)
                generated_files.append(output_file)

            # Show success message with file locations
            QMessageBox.information(
                self,
                "Success",
                f"Documents generated successfully!\n\nLocation: {output_dir}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

from PyQt6.QtWidgets import QApplication
import sys
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

from ui import main

if __name__ == "__main__":
    main()