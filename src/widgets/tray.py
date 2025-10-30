"""System tray widget module."""

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QActionGroup, QIcon, QPixmap
from PySide6.QtWidgets import QMenu, QSystemTrayIcon

from src.config import texts
from src.constants.path import Files
from src.constants.settings import MOVE_TIMER_HOTKEY, POMODORO_MODE_MIN, STANDARD_MODE_MIN


class SystemTray(QSystemTrayIcon):
    """System tray icon with menu for application control."""

    quit_requested = Signal()
    autostart_toggled = Signal(bool)
    online_wallpapers_toggled = Signal(bool)
    work_mode_changed = Signal(int)  # duration in minutes
    move_timer_requested = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        """Initialize the system tray.

        Args:
            parent: The parent object.

        """
        super().__init__(parent)

        # Load icon
        icon_path = Files.ICON_PATH
        if icon_path.exists():
            self.setIcon(QIcon(str(icon_path)))
        else:
            # Fallback to a simple icon
            pixmap = QPixmap(16, 16)
            pixmap.fill(Qt.GlobalColor.gray)
            self.setIcon(QIcon(pixmap))

        # Create menu
        self._create_menu()

        # Connect signals
        self.activated.connect(self._on_activated)

    def _create_menu(self) -> None:
        """Create the system tray menu."""
        menu = QMenu()

        # Autostart toggle action
        self.autostart_action = menu.addAction(texts.Tray.MENU_AUTOSTART)
        self.autostart_action.setCheckable(True)
        self.autostart_action.triggered.connect(self._on_autostart_toggled)

        # Online wallpapers toggle action
        self.online_wallpapers_action = menu.addAction(texts.Tray.MENU_ONLINE_WALLPAPERS)
        self.online_wallpapers_action.setCheckable(True)
        self.online_wallpapers_action.triggered.connect(self._on_online_wallpapers_toggled)

        menu.addSeparator()

        # Work mode submenu
        work_mode_menu = menu.addMenu(texts.Tray.MENU_WORK_MODE)
        self.work_mode_group = QActionGroup(self)

        # Pomodoro mode
        self.mode_25_action = work_mode_menu.addAction(
            f"🚀 {POMODORO_MODE_MIN} минут (Pomodoro)",
        )
        self.mode_25_action.setCheckable(True)
        self.mode_25_action.setData(POMODORO_MODE_MIN)
        self.mode_25_action.triggered.connect(
            lambda: self._on_work_mode_changed(POMODORO_MODE_MIN),
        )
        self.work_mode_group.addAction(self.mode_25_action)

        # Standard mode
        self.mode_45_action = work_mode_menu.addAction(
            f"⏳ {STANDARD_MODE_MIN} минут (Стандартный)",
        )
        self.mode_45_action.setCheckable(True)
        self.mode_45_action.setData(STANDARD_MODE_MIN)
        self.mode_45_action.triggered.connect(
            lambda: self._on_work_mode_changed(STANDARD_MODE_MIN),
        )
        self.work_mode_group.addAction(self.mode_45_action)

        menu.addSeparator()

        # Move timer action (with hotkey display)
        move_timer_action = menu.addAction(
            f"⚙️ {texts.Tray.MENU_MOVE_TIMER} ({MOVE_TIMER_HOTKEY.upper()})",
        )
        move_timer_action.triggered.connect(self._on_move_timer_requested)

        # Quit action
        self.quit_action = menu.addAction(texts.Tray.MENU_QUIT)
        self.quit_action.triggered.connect(self._on_quit_requested)

        self.setContextMenu(menu)

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """Handle tray icon activation.

        Args:
            reason: The activation reason.

        """
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.showMessage(
                texts.Tray.MESSAGE_TITLE,
                texts.Tray.MESSAGE_INFO,
                QSystemTrayIcon.MessageIcon.Information,
            )

    def _on_autostart_toggled(self, checked: bool) -> None:
        """Handle autostart toggle.

        Args:
            checked: The checked state.

        """
        self.autostart_toggled.emit(checked)

    def _on_quit_requested(self) -> None:
        """Handle quit request."""
        self.quit_requested.emit()

    def _on_online_wallpapers_toggled(self, checked: bool) -> None:
        """Handle online wallpapers toggle.

        Args:
            checked: The checked state.

        """
        self.online_wallpapers_toggled.emit(checked)

    def _on_work_mode_changed(self, duration: int) -> None:
        """Handle work mode change.

        Args:
            duration: Work duration in minutes (25 or 45).

        """
        self.work_mode_changed.emit(duration)

    def _on_move_timer_requested(self) -> None:
        """Handle move timer request."""
        self.move_timer_requested.emit()

    def set_autostart_enabled(self, enabled: bool) -> None:
        """Set the autostart menu item state.

        Args:
            enabled: True if autostart is enabled, False otherwise.

        """
        self.autostart_action.setChecked(enabled)

    def set_quit_enabled(self, enabled: bool) -> None:
        """Set the quit menu item enabled state.

        Args:
            enabled: True if quit should be enabled, False otherwise.

        """
        self.quit_action.setEnabled(enabled)

    def set_online_wallpapers_enabled(self, enabled: bool) -> None:
        """Set the online wallpapers menu item state.

        Args:
            enabled: True if online wallpapers is enabled, False otherwise.

        """
        self.online_wallpapers_action.setChecked(enabled)

    def update_state(self, is_work_active: bool, is_break_active: bool) -> None:
        """Update tray icon and menu based on current state.

        Args:
            is_work_active: True if work timer is active.
            is_break_active: True if break timer is active.

        """
        if is_break_active:
            self.setToolTip(texts.Tray.TOOLTIP_BREAK)
            self.set_quit_enabled(False)
        elif is_work_active:
            self.setToolTip(texts.Tray.TOOLTIP_WORK)
            self.set_quit_enabled(True)
        else:
            self.setToolTip(texts.Tray.TOOLTIP_WAITING)
            self.set_quit_enabled(True)

    def set_work_mode(self, duration: int) -> None:
        """Set the work mode menu item state.

        Args:
            duration: Work duration in minutes (25 or 45).

        """
        if duration == POMODORO_MODE_MIN:
            self.mode_25_action.setChecked(True)
        elif duration == STANDARD_MODE_MIN:
            self.mode_45_action.setChecked(True)
