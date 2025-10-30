"""Application orchestrator for Take Break app."""

import sys
from datetime import UTC, datetime

import keyboard
from loguru import logger
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication, QDialog

from src.config import texts
from src.config.settings import Settings
from src.constants.settings import (
    BREAK_DURATION_MIN,
    MOVE_TIMER_HOTKEY,
    POMODORO_MODE_MIN,
    TIMER_INTERVAL_MS,
)
from src.db.db import Database
from src.services import autostart
from src.services.position import (
    WidgetPosition,
    calculate_position,
    get_next_position,
)
from src.services.timer import TimerManager
from src.widgets.overlay import BlockingOverlay
from src.widgets.timer import TimerWidget
from src.widgets.tray import SystemTray
from src.widgets.welcome import WelcomeDialog


class App:
    """Application orchestrator.

    Coordinates interaction between services and widgets without
    containing business logic. Knows WHEN to call methods but not HOW
    they work internally.
    """

    def __init__(self) -> None:
        """Initialize the application.

        Creates the QApplication, initializes all components (services and widgets),
        and wires up connections between them.
        """
        logger.debug("Initializing application")
        self.app = QApplication(sys.argv)
        self.width = self.app.primaryScreen().geometry().width()
        self.height = self.app.primaryScreen().geometry().height()

        self.overlay = BlockingOverlay(screen_width=self.width, screen_height=self.height)
        # Initialize services
        self.timer_manager = TimerManager()
        self.settings = Settings(db=Database())

        # Initialize widgets
        self.timer_widget = TimerWidget()
        self.tray = SystemTray()

        # Initialize timer position
        self.current_position = WidgetPosition.TOP_RIGHT

        # Initialize Qt timer for periodic updates
        self.timer = QTimer()
        self.timer.timeout.connect(self._on_timer_timeout)

        # Load focus and work mode from settings
        self.focus_text = self.settings.get_focus()
        self.work_duration = self.settings.get_work_duration()

        # Initialize extra rest timer
        self._extra_rest_start: datetime | None = None

        # Configure key handling
        self.overlay.keyPressEvent = self._handle_key_press

        # Connect overlay close signal
        self.overlay.close_requested.connect(self.quit)

        # Configure global hotkeys
        self._setup_hotkeys()

        # Configure tray signals
        self._setup_tray()

        # Load and apply online wallpapers setting
        use_online = self.settings.get_use_online_wallpapers()
        self.overlay.wallpaper_manager.set_use_online(use_online)
        self.tray.set_online_wallpapers_enabled(use_online)

        # Check for first run and show welcome dialog
        if self.settings.is_first_run():
            self._show_welcome_dialog()

        # Show initial overlay
        self.show_initial_overlay()

        # Show tray icon
        self.tray.show()

        logger.info("Application initialized and ready to work")

    def _setup_hotkeys(self) -> None:
        """Configure global application hotkeys."""
        # Load hotkey from JSON or save default
        hotkey = self.settings.get_move_timer_hotkey()
        if not hotkey:
            hotkey = MOVE_TIMER_HOTKEY
            self.settings.set_move_timer_hotkey(hotkey)
        keyboard.add_hotkey(hotkey, self._move_timer)

    def _setup_tray(self) -> None:
        """Configure system tray signals and initial state."""
        # Connect signals
        self.tray.quit_requested.connect(self.quit)
        self.tray.autostart_toggled.connect(self._on_autostart_toggle)
        self.tray.online_wallpapers_toggled.connect(self._on_online_wallpapers_toggle)
        self.tray.work_mode_changed.connect(self._on_work_mode_changed)
        self.tray.move_timer_requested.connect(self._move_timer)

        # Set initial autostart state
        self.tray.set_autostart_enabled(autostart.is_autostart_enabled())

        # Set initial work mode
        self.tray.set_work_mode(self.work_duration)

        # Update initial state
        self._update_tray_state()

    def _show_welcome_dialog(self) -> None:
        """Show welcome dialog on first run."""
        dialog = WelcomeDialog()
        result = dialog.exec()

        # If user rejected (Cancel or closed), quit the application
        if result == QDialog.DialogCode.Rejected:
            logger.info("User declined to start the application")
            self.quit()
            sys.exit(0)

        # Get selected work duration and save it
        selected_duration = dialog.get_selected_work_duration()
        self.settings.set_work_duration(selected_duration)
        self.work_duration = selected_duration
        self.tray.set_work_mode(selected_duration)

        self.settings.mark_first_run_complete()
        logger.info("Welcome dialog accepted and first run marked")

    def _on_autostart_toggle(self, enabled: bool) -> None:
        """Handle autostart toggle from tray menu.

        Args:
            enabled: True to enable autostart, False to disable.

        """
        if enabled:
            autostart.enable_autostart()
        else:
            autostart.disable_autostart()
        logger.info(f"Autostart toggled: {enabled}")

    def _on_online_wallpapers_toggle(self, enabled: bool) -> None:
        """Handle online wallpapers toggle from tray menu.

        Args:
            enabled: True to enable online wallpapers, False to use local only.

        """
        self.settings.set_use_online_wallpapers(enabled)
        self.overlay.wallpaper_manager.set_use_online(enabled)
        logger.info(f"Online wallpapers toggled: {enabled}")

    def _on_work_mode_changed(self, duration: int) -> None:
        """Handle work mode change from tray menu.

        Args:
            duration: Work duration in minutes (25 or 45).

        """
        self.work_duration = duration
        self.settings.set_work_duration(duration)
        self.tray.set_work_mode(duration)

        # Show notification
        mode_name = (
            texts.WorkModes.POMODORO if duration == POMODORO_MODE_MIN else texts.WorkModes.STANDARD
        )
        message = f"Режим изменён на {duration} мин ({mode_name}). Применится после текущего цикла"
        self.tray.showMessage(
            texts.Tray.MESSAGE_TITLE,
            message,
            self.tray.MessageIcon.Information,
            3000,
        )
        logger.info(f"Work mode changed to {duration} minutes")

    def _update_tray_state(self) -> None:
        """Update tray icon and menu state based on current timer state."""
        is_work_active = self.timer_manager.is_work_active()
        is_break_active = self.timer_manager.is_break_active()
        self.tray.update_state(is_work_active, is_break_active)

    def _move_timer(self) -> None:
        """Orchestrate timer position change."""
        self.current_position = get_next_position(self.current_position)
        self._reposition_timer()
        logger.debug(f"Timer moved to {self.current_position.name}")

    def _reposition_timer(self) -> None:
        """Reposition the timer widget on the screen."""
        if not (screen := self.app.primaryScreen()):
            return

        screen_geometry = screen.availableGeometry()  # Учитывает панель задач

        # Widget has fixed size, no need to adjust
        widget_size = self.timer_widget.size()

        position = calculate_position(
            self.current_position,
            screen_geometry.width(),
            screen_geometry.height(),
            widget_size.width(),
            widget_size.height(),
        )

        # Adjust position relative to available geometry
        x = screen_geometry.x() + position.x()
        y = screen_geometry.y() + position.y()

        self.timer_widget.move(x, y)

    def show_initial_overlay(self) -> None:
        """Show the initial overlay for selecting a work mode."""
        # Set text based on whether there's a previous focus
        overlay_text = texts.Overlay.get_initial_text(
            self.focus_text if self.focus_text else None,
            self.work_duration,
        )
        self.overlay.set_text(overlay_text)

        # Pre-fill the focus input with previous focus if available
        if self.focus_text:
            self.overlay.set_focus_text(self.focus_text)

        # Show focus input field
        self.overlay.show_focus_input()

        # Show extra rest timer if active
        if self._extra_rest_start:
            self.overlay.show_extra_rest_timer(self._extra_rest_start)

        self.overlay.show()

    def _handle_key_press(self, event: QKeyEvent | None) -> None:
        """Handle key presses on the overlay.

        Args:
            event: The key press event.

        """
        if event is None:
            return

        key = event.key()

        if key == Qt.Key.Key_Return:
            # Ignore Enter during break
            if self.timer_manager.is_break_active():
                logger.warning("Cannot start work during break")
                return

            self.focus_text = self.overlay.get_focus_text()
            # Save focus to disk
            self.settings.save_focus(self.focus_text)
            self.overlay.hide()
            self.start_work_timer()
            logger.info(f"Work timer started with focus: {self.focus_text}")

    def start_work_timer(self) -> None:
        """Orchestrate work timer start."""
        if self.timer_manager.is_break_active():
            logger.warning("Attempt to start timer during break")
            return

        # Get current work duration from settings (may have changed)
        self.work_duration = self.settings.get_work_duration()

        # Reset extra rest timer
        self._extra_rest_start = None

        self.timer_manager.start_work(self.work_duration)
        self.timer_widget.set_focus_text(self.focus_text)
        self.timer_widget.show()

        # Position after widget is fully rendered in the event loop
        QTimer.singleShot(0, self._reposition_timer)

        self.timer.start(TIMER_INTERVAL_MS)
        self._update_tray_state()
        logger.info(f"Work timer started for {self.work_duration} minutes")

    def start_break_timer(self) -> None:
        """Orchestrate break timer start."""
        self.timer_manager.start_break()
        self.overlay.is_blocking = True
        self.overlay.hide_focus_input()
        self.overlay.hide_extra_rest_timer()  # Скрыть доп отдых
        self.overlay.set_text(texts.Overlay().break_message)  # type: ignore[attr-defined]
        self.overlay.show()
        self._update_tray_state()
        logger.info(f"Break started for {BREAK_DURATION_MIN} minutes")

    def _on_timer_timeout(self) -> None:
        """Orchestrate timer updates.

        Coordinates UI updates based on timer state without containing logic.
        """
        # Work timer
        if self.timer_manager.is_work_expired():
            logger.debug("Work time expired")
            self.start_break_timer()
        elif self.timer_manager.is_work_active():
            remaining = self.timer_manager.get_work_remaining()
            if remaining:
                self.timer_widget.update_time(remaining)

        # Break timer
        if self.timer_manager.is_break_expired():
            logger.debug("Break time expired")
            self.end_break()
        elif self.timer_manager.is_break_active():
            remaining = self.timer_manager.get_break_remaining()
            if remaining:
                self.overlay.update_time(remaining)

    def end_break(self) -> None:
        """Orchestrate break end and return to initial state."""
        self.timer_manager.end_break()

        # Start extra rest timer
        self._extra_rest_start = datetime.now(UTC)

        # Don't overwrite focus_text here - keep the existing focus
        self.overlay.is_blocking = False
        self.overlay.show_focus_input()
        self.overlay.hide()
        self.timer_widget.hide()
        self.timer_widget.reset_style()
        self.timer.stop()
        self._update_tray_state()
        self.show_initial_overlay()
        logger.info("Break ended, extra rest timer started")

    def quit(self) -> None:
        """Quit the application.

        Prevents quitting during an active break.
        """
        if self.timer_manager.is_break_active():
            logger.warning("Cannot quit during break")
            return
        keyboard.unhook_all()
        self.app.quit()

    def run(self) -> int:
        """Run the main application loop.

        Returns:
            The application's exit code.

        """
        return self.app.exec()
