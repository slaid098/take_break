"""Module for displaying the timer widget."""

from datetime import timedelta

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPaintEvent
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from src.constants.settings import RED_SECOND_THRESHOLD
from src.utils.time import format_time
from src.widgets.styles import (
    TIMER_FOCUS_STYLE,
    TIMER_TIME_RED_STYLE,
    TIMER_TIME_STYLE,
    TIMER_WIDGET_STYLE,
)


class TimerWidget(QWidget):
    """Widget for displaying the timer."""

    def __init__(self) -> None:
        """Initialize the timer widget.

        Sets up window flags and appearance, and creates UI elements.
        """
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool,
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Apply widget background style
        self.setStyleSheet(TIMER_WIDGET_STYLE)

        # Set up the interface
        layout = QVBoxLayout()
        self.time_label = QLabel()
        self.focus_label = QLabel()

        # Center align labels
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.focus_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.reset_style()

        # Add padding inside widget
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)

        layout.addWidget(self.time_label)
        layout.addWidget(self.focus_label)
        self.setLayout(layout)

        # Set minimum dimensions based on time label only
        self.time_label.setText("00:00")
        self.focus_label.hide()
        self.adjustSize()

        min_height = self.sizeHint().height()
        self.setMinimumHeight(min_height)
        self.setMinimumWidth(180)

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        """Paint the widget background with transparency."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw semi-transparent rounded rectangle background
        rect = self.rect()
        bg_color = QColor(0, 0, 0, 150)  # Semi-transparent black
        painter.setBrush(bg_color)
        painter.drawRoundedRect(rect, 10, 10)

        # Draw white border
        border_color = QColor(255, 255, 255, 20)
        painter.setPen(border_color)
        painter.setBrush(Qt.GlobalColor.transparent)
        painter.drawRoundedRect(rect, 10, 10)

        super().paintEvent(event)

    def set_focus_text(self, text: str) -> None:
        """Set the focus text.

        Args:
            text: The focus text to be displayed.

        """
        if text:
            self.focus_label.setText(f"🎯 {text}")
            self.focus_label.setVisible(True)
        else:
            self.focus_label.setText("")
            self.focus_label.setVisible(False)

        # Adjust size based on content
        self.adjustSize()

    def reset_style(self) -> None:
        """Reset the widget's style to its initial state."""
        self.time_label.setStyleSheet(TIMER_TIME_STYLE)
        self.focus_label.setStyleSheet(TIMER_FOCUS_STYLE)
        # Don't hide focus_label here - it should stay visible if set

    def update_time(self, remaining: timedelta) -> None:
        """Update the displayed time.

        If less than a minute remains, the style changes to red.

        Args:
            remaining: The remaining time.

        """
        # Color in red if less than a minute remains
        if remaining.total_seconds() <= RED_SECOND_THRESHOLD:
            self._paint_it_red()
        else:
            # Update only time style, keep focus visible
            self.time_label.setStyleSheet(TIMER_TIME_STYLE)

        self.time_label.setText(format_time(remaining))

    def _paint_it_red(self) -> None:
        """Paint the timer in red."""
        self.time_label.setStyleSheet(TIMER_TIME_RED_STYLE)

