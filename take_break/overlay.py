"""Blocking overlay window module."""

from datetime import timedelta

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QImage, QPainter, QPaintEvent, QShowEvent
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class BlockingOverlay(QWidget):
    """Blocking overlay window that covers the entire screen."""

    def __init__(self) -> None:
        """Initialize the overlay."""
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool,
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        # Set up the layout
        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
                background-color: rgba(0, 0, 0, 180);
                border-radius: 10px;
            }
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def showEvent(self, a0: QShowEvent | None) -> None:
        """Handle show event to cover the entire screen."""
        if screen := self.screen():
            self.setGeometry(screen.geometry())
        if a0 is not None:
            super().showEvent(a0)

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        """Paint the overlay with strong blur effect."""
        painter = QPainter(self)

        # Create a very strong blur effect
        rect = self.rect()

        # Create multiple semi-transparent layers
        for i in range(10):
            opacity = 200 - i * 5  # Start from more opaque and gradually decrease
            painter.fillRect(rect, QColor(0, 0, 0, opacity))

        # Add noise pattern for additional obscurity
        noise_size = QSize(rect.width(), rect.height())
        noise = QImage(noise_size, QImage.Format.Format_ARGB32_Premultiplied)
        noise.fill(QColor(0, 0, 0, 30))

        for x in range(0, rect.width(), 2):
            for y in range(0, rect.height(), 2):
                if (x + y) % 4 == 0:
                    noise.setPixelColor(x, y, QColor(255, 255, 255, 10))

        painter.drawImage(rect, noise)

        if a0 is not None:
            super().paintEvent(a0)

    def setText(self, text: str) -> None:
        """Set overlay text."""
        self.label.setText(text)

    def update_time(self, remaining: timedelta) -> None:
        """Update remaining time display."""
        minutes = int(remaining.total_seconds() // 60)
        seconds = int(remaining.total_seconds() % 60)
        self.setText(f"Break: {minutes:02d}:{seconds:02d}")

    def show(self) -> None:
        """Show overlay and set focus."""
        super().show()
        self.activateWindow()
        self.setFocus(Qt.FocusReason.PopupFocusReason)
