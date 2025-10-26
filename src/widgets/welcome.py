"""Welcome dialog widget module."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from src.config import settings, texts
from src.config.texts import WelcomeDialogTexts
from src.widgets.styles import (
    WELCOME_BUTTONS_STYLE,
    WELCOME_DESCRIPTION_STYLE,
    WELCOME_DIALOG_STYLE,
    WELCOME_SUBTITLE_STYLE,
    WELCOME_TITLE_STYLE,
)


class WelcomeDialog(QDialog):
    """Welcome dialog shown on first application launch."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the welcome dialog.

        Args:
            parent: The parent widget.

        """
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the welcome dialog UI."""
        self.setWindowTitle(texts.AppInfo.TITLE)
        self.setFixedSize(620, 520)
        self.setModal(True)

        # Set dialog background
        self.setStyleSheet(WELCOME_DIALOG_STYLE)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)

        # Title
        title_label = QLabel(texts.WelcomeDialog.TITLE)
        title_label.setStyleSheet(WELCOME_TITLE_STYLE)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel(texts.WelcomeDialog.SUBTITLE)
        subtitle_label.setStyleSheet(WELCOME_SUBTITLE_STYLE)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)

        # Description box
        texts_instance = WelcomeDialogTexts()
        description_label = QLabel(texts_instance.description)
        description_label.setWordWrap(True)
        description_label.setStyleSheet(WELCOME_DESCRIPTION_STYLE)
        layout.addWidget(description_label)

        # Work mode selector
        work_mode_selector = self._create_work_mode_selector()
        layout.addWidget(work_mode_selector)

        layout.addStretch()

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
        )
        button_box.button(QDialogButtonBox.StandardButton.Ok).setText(texts.WelcomeDialog.BUTTON_START)
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setText(texts.WelcomeDialog.BUTTON_CANCEL)
        button_box.setStyleSheet(WELCOME_BUTTONS_STYLE)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def _create_work_mode_selector(self) -> QWidget:
        """Create work mode selector with radio buttons.

        Returns:
            Container widget with work mode selection.

        """
        container = QWidget()
        layout = QVBoxLayout()

        # Label
        label = QLabel("Выберите режим работы:")
        label.setStyleSheet("font-size: 14px; color: #2c3e50; font-weight: bold;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Radio buttons
        radio_layout = QHBoxLayout()
        radio_layout.setSpacing(30)

        self.work_mode_group = QButtonGroup()

        self.radio_25 = QRadioButton(f"🚀 {settings.POMODORO_MODE_MIN} минут (Pomodoro)")
        self.radio_25.setStyleSheet("font-size: 13px;")
        self.work_mode_group.addButton(self.radio_25, settings.POMODORO_MODE_MIN)

        self.radio_45 = QRadioButton(f"⏳ {settings.STANDARD_MODE_MIN} минут (Стандартный)")
        self.radio_45.setStyleSheet("font-size: 13px;")
        self.radio_45.setChecked(True)  # Default
        self.work_mode_group.addButton(self.radio_45, settings.STANDARD_MODE_MIN)

        radio_layout.addStretch()
        radio_layout.addWidget(self.radio_25)
        radio_layout.addWidget(self.radio_45)
        radio_layout.addStretch()

        layout.addLayout(radio_layout)
        container.setLayout(layout)
        return container

    def get_selected_work_duration(self) -> int:
        """Get the selected work duration.

        Returns:
            Selected work duration in minutes.

        """
        return self.work_mode_group.checkedId()
