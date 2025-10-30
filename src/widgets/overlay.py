"""Blocking overlay window module for Take Break application."""

from datetime import UTC, datetime, timedelta

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QCloseEvent, QKeyEvent, QPainter, QPaintEvent, QShowEvent
from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWidget

from src.config import texts
from src.constants.settings import MAX_FOCUS_LENGTH
from src.services.wallpaper import WallpaperManager
from src.utils.time import format_time
from src.widgets.background import paint_background
from src.widgets.styles import EXTRA_REST_LABEL_STYLE, OVERLAY_INPUT_STYLE, OVERLAY_LABEL_STYLE


class BlockingOverlay(QWidget):
    """A blocking overlay window that covers the entire screen.

    This widget is designed to be a frameless, always-on-top window that
    captures all user input during a break session. It displays a wallpaper,
    a countdown timer, and an input field for the user's focus.

    Attributes:
        close_requested (Signal): Emitted when the window is allowed to close.

    """

    close_requested = Signal()

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """Initialize the overlay window.

        Sets up the window's appearance, wallpaper manager, UI elements,
        and internal state.

        Args:
            screen_width: The width of the screen.
            screen_height: The height of the screen.

        """
        super().__init__()
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._setup_wallpaper_manager()
        self._setup_window_config()
        self._create_ui_elements()
        self._setup_layout()
        self.is_blocking = False
        self.extra_rest_start: datetime | None = None

    def _setup_window_config(self) -> None:
        """Configure the window's appearance and behavior.

        Sets the window to be frameless and always on top, which is essential
        for a blocking overlay. It also enables a translucent background to allow
        for custom rounded corners or other non-rectangular shapes if needed.
        """
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint,
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _setup_wallpaper_manager(self) -> None:
        """Initialize the wallpaper manager."""
        self.wallpaper_manager = WallpaperManager(
            width=self._screen_width,
            height=self._screen_height,
        )

    def _create_ui_elements(self) -> None:
        """Create all UI elements for the overlay."""
        self._create_main_label()
        self._create_focus_input()
        self._create_extra_rest_label()

    def _create_main_label(self) -> None:
        """Create the main text label for displaying timers."""
        self.label = QLabel()
        self.label.setStyleSheet(OVERLAY_LABEL_STYLE)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setTextFormat(Qt.TextFormat.RichText)

    def _create_focus_input(self) -> None:
        """Create the focus input field."""
        self.focus_input = QLineEdit()
        self.focus_input.setPlaceholderText(texts.Overlay.PLACEHOLDER)
        self.focus_input.setMaxLength(MAX_FOCUS_LENGTH)
        self.focus_input.setStyleSheet(OVERLAY_INPUT_STYLE)
        self.focus_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font_metrics = self.focus_input.fontMetrics()
        char_width = font_metrics.horizontalAdvance("M")
        text_width = char_width * (MAX_FOCUS_LENGTH + 2)
        total_width = text_width + 24 + 4 + 40  # Padding + Border + Margin
        self.focus_input.setFixedWidth(total_width)

    def _create_extra_rest_label(self) -> None:
        """Create the label and timer for the extra rest period."""
        self.extra_rest_label = QLabel()
        self.extra_rest_label.setStyleSheet(EXTRA_REST_LABEL_STYLE)
        self.extra_rest_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.extra_rest_label.hide()
        self.extra_rest_timer = QTimer()
        self.extra_rest_timer.timeout.connect(self._update_extra_rest_timer)

    def _setup_layout(self) -> None:
        """Arranges UI elements in a centered vertical layout."""
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.focus_input, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.extra_rest_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        """Handle key press events.

        Specifically blocks the Escape key from closing the window when in
        blocking mode.

        Args:
            event: The QKeyEvent object.

        """
        if event.key() == Qt.Key.Key_Escape and self.is_blocking:
            event.ignore()
            return

        super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        """Handle the window close event.

        Prevents the window from being closed (e.g., via Alt+F4) while
        `is_blocking` is True.

        Args:
            event: The QCloseEvent object.

        """
        if self.is_blocking:
            event.ignore()
        else:
            event.accept()
            self.close_requested.emit()

    def showEvent(self, event: QShowEvent) -> None:  # noqa: N802
        """Handle the window show event.

        Selects a random wallpaper to be displayed when the window becomes visible.

        Args:
            event: The QShowEvent object.

        """
        self._current_wallpaper = self.wallpaper_manager.get_wallpaper()
        super().showEvent(event)
        self.update()  # Trigger a repaint with the new wallpaper

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        """Handle the window paint event.

        Draws the current wallpaper as the background with a dark tint.

        Args:
            event: The QPaintEvent object.

        """
        painter = QPainter(self)
        paint_background(painter, self.rect(), self._current_wallpaper)
        super().paintEvent(event)

    def set_text(self, text: str) -> None:
        """Set the text for the main overlay label.

        Args:
            text: The text to be displayed.

        """
        self.label.setText(text)

    def get_focus_text(self) -> str:
        """Return the text from the focus input field.

        Returns:
            The text entered by the user.

        """
        return self.focus_input.text()

    def update_time(self, remaining: timedelta) -> None:
        """Update the display of the remaining time on the main label.

        Args:
            remaining: A timedelta object representing the remaining time.

        """
        self.set_text(f"Break: {format_time(remaining)}")

    def set_focus_text(self, text: str) -> None:
        """Set the focus text in the input field.

        Args:
            text: The focus text to be displayed.

        """
        self.focus_input.setText(text)

    def hide_focus_input(self) -> None:
        """Hides the focus input field."""
        self.focus_input.hide()

    def show_focus_input(self) -> None:
        """Show the focus input field."""
        self.focus_input.show()

    def hide_extra_rest_timer(self) -> None:
        """Hide and stops the extra rest timer."""
        self.extra_rest_label.hide()
        self.extra_rest_timer.stop()
        self.extra_rest_start = None

    def show_extra_rest_timer(self, start_time: datetime) -> None:
        """Show and starts the extra rest timer.

        Args:
            start_time: The UTC datetime when the extra rest period began.

        """
        self.extra_rest_start = start_time
        self._update_extra_rest_timer()
        self.extra_rest_label.show()
        self.extra_rest_timer.start(1000)

    def _update_extra_rest_timer(self) -> None:
        """Update the text of the extra rest timer label every second."""
        if self.extra_rest_start is None:
            self.hide_extra_rest_timer()
            return

        elapsed = datetime.now(UTC) - self.extra_rest_start
        total_seconds = int(elapsed.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if hours > 0:
            text = f"☕ Дополнительный отдых: +{hours:d}ч {minutes:02d}:{seconds:02d}"
        else:
            text = f"☕ Дополнительный отдых: +{minutes:02d}:{seconds:02d}"
        self.extra_rest_label.setText(text)

    def show(self) -> None:
        """Show the overlay in true fullscreen mode.

        This is the key method for ensuring a non-bypassable block.
        `showFullScreen` correctly covers the entire screen, including the
        taskbar, and takes focus.
        """
        self.showFullScreen()
        self.activateWindow()
        self.raise_()
