from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class LoadingIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout()
        self.label = QLabel("Generating documents...")
        self.label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 14px;
                padding: 10px;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)