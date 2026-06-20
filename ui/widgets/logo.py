from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QPixmap, QFont, QColor
from PyQt6.QtCore import Qt, QRect, QSize

class LogoWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(QSize(200, 60))
        self.generate_logo()

    def generate_logo(self):
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw circular icon
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(254, 159, 43))  # Brand color
        painter.drawEllipse(QRect(5, 10, 40, 40))

        # Draw "R" in circle
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 20, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(QRect(15, 10, 40, 40), Qt.AlignmentFlag.AlignCenter, "R")

        # Draw app name
        painter.setPen(QColor(44, 62, 80))  # Dark text color
        font = QFont("Arial", 18, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(QRect(55, 10, 140, 40), Qt.AlignmentFlag.AlignVCenter, "Resume.ai")

        painter.end()
        self.setPixmap(pixmap)