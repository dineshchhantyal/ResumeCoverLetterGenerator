from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLineEdit, QPushButton, QRadioButton, QButtonGroup,
                           QLabel, QMessageBox, QTabWidget, QSplitter, QFrame)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPalette
import os
from datetime import datetime
from resume.generator import ResumeGenerator
from coverletter.generator import CoverLetterGenerator
from .editors.yaml_editor import YamlEditor
from .widgets.loading_indicator import LoadingIndicator
from .widgets.logo import LogoWidget
import subprocess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.apply_styles()
        self.loading = LoadingIndicator(self)
        self.loading.hide()

    def init_ui(self):
        self.setWindowTitle("Resume & Cover Letter Generator")
        self.setGeometry(100, 100, 1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Left panel for inputs
        left_panel = QFrame()
        left_panel.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(15)

        # Add logo at the top
        logo = LogoWidget()
        left_layout.insertWidget(0, logo, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Add spacing after logo
        left_layout.insertSpacing(1, 20)

        # Input fields with modern styling
        title_label = QLabel("Document Generator")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)

        self.company_name = QLineEdit()
        self.company_name.setPlaceholderText("Enter Company Name")
        self.company_name.setObjectName("inputField")
        left_layout.addWidget(self.company_name)

        self.role_name = QLineEdit()
        self.role_name.setPlaceholderText("Enter Role Name")
        self.role_name.setObjectName("inputField")
        left_layout.addWidget(self.role_name)

        # Radio buttons in a container
        radio_container = QFrame()
        radio_container.setObjectName("radioContainer")
        radio_layout = QVBoxLayout(radio_container)

        self.btn_group = QButtonGroup()
        self.resume_only = QRadioButton("Resume Only")
        self.cover_only = QRadioButton("Cover Letter Only")
        self.both = QRadioButton("Both Documents")

        for btn in [self.resume_only, self.cover_only, self.both]:
            btn.setObjectName("radioButton")
            self.btn_group.addButton(btn)
            radio_layout.addWidget(btn)

        self.both.setChecked(True)
        left_layout.addWidget(radio_container)

        # Generate button
        self.generate_btn = QPushButton("Generate Documents")
        self.generate_btn.setObjectName("generateButton")
        self.generate_btn.clicked.connect(self.generate_documents)
        left_layout.addWidget(self.generate_btn)

        left_layout.addStretch()
        main_layout.addWidget(left_panel)

        # Right panel - Editors
        editors = QTabWidget()
        resume_editor = YamlEditor("resume/resume.yml")
        cover_letter_editor = YamlEditor("coverletter/coverletter.yml")

        editors.addTab(resume_editor, "Resume")
        editors.addTab(cover_letter_editor, "Cover Letter")

        main_layout.addWidget(editors)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            #leftPanel {
                background-color: white;
                border-radius: 10px;
                min-width: 300px;
                max-width: 400px;
            }
            #titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 20px;
            }
            #inputField {
                padding: 12px;
                border: 2px solid #eee;
                border-radius: 8px;
                font-size: 14px;
                margin-bottom: 10px;
            }
            #inputField:focus {
                border-color: rgb(254, 159, 43);
            }
            #radioContainer {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
            }
            #radioButton {
                padding: 8px;
                font-size: 14px;
            }
            #radioButton::indicator {
                width: 18px;
                height: 18px;
            }
            #radioButton::indicator:checked {
                background-color: rgb(254, 159, 43);
            }
            #generateButton {
                background-color: rgb(254, 159, 43);
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            #generateButton:hover {
                background-color: rgb(234, 139, 23);
            }
        """)

    def get_choice(self):
        if self.resume_only.isChecked():
            return "1"
        elif self.cover_only.isChecked():
            return "2"
        return "3"

    def generate_documents(self):
        try:
            company_name = self.company_name.text().strip()
            role_name = self.role_name.text().strip()

            if not company_name or not role_name:
                QMessageBox.warning(self, "Input Error",
                                  "Company name and role name are required!")
                return

            # Show loading indicator
            self.loading.move(
                self.frameGeometry().center() - self.loading.rect().center()
            )
            self.loading.show()
            self.generate_btn.setEnabled(False)

            # Use timer to allow UI update
            QTimer.singleShot(100, lambda: self._generate_docs(company_name, role_name))

        except Exception as e:
            self.loading.hide()
            self.generate_btn.setEnabled(True)
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def _generate_docs(self, company_name, role_name):
        try:
            base_dir = os.getcwd()
            output_dir = self.create_output_structure(base_dir, company_name, role_name)
            choice = self.get_choice()
            generated_files = []

            if choice in ['1', '3']:
                resume_file = os.path.join(output_dir, 'resume.pdf')
                resume_generator = ResumeGenerator(
                    os.path.join(base_dir, "resume", "resume.yml"))
                output_file = resume_generator.generate_pdf(resume_file, output_dir)
                generated_files.append(output_file)

            if choice in ['2', '3']:
                cover_letter_file = os.path.join(output_dir, 'cover_letter.pdf')
                coverletter_generator = CoverLetterGenerator(
                    os.path.join(base_dir, "coverletter", "coverletter.yml"))
                output_file = coverletter_generator.generate_pdf(
                    cover_letter_file, output_dir, company_name)
                generated_files.append(output_file)

            # Hide loading and enable button
            self.loading.hide()
            self.generate_btn.setEnabled(True)

            # Show success message with option to open folder
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("Documents generated successfully!")
            msg.setInformativeText(f"Location: {output_dir}")
            msg.setWindowTitle("Success")

            open_btn = msg.addButton("Open Folder", QMessageBox.ButtonRole.ActionRole)
            msg.addButton(QMessageBox.StandardButton.Ok)

            msg.exec()

            if msg.clickedButton() == open_btn:
                self.open_folder(output_dir)

        except Exception as e:
            self.loading.hide()
            self.generate_btn.setEnabled(True)
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def open_folder(self, path):
        try:
            subprocess.run(['open', path], check=True)
        except subprocess.CalledProcessError:
            QMessageBox.warning(self, "Warning",
                              "Could not open folder in Finder")

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