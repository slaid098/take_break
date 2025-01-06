"""Main module of Take Break application."""

import sys
from datetime import datetime, timedelta
from enum import Enum, auto

import keyboard
from loguru import logger
from PyQt6.QtCore import QPoint, Qt, QTimer
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QApplication

from .blocker import InputBlocker
from .overlay import BlockingOverlay
from .timer_widget import TimerWidget


class TimerPosition(Enum):
    """Timer widget position on screen."""
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()


class TakeBreakApp:
    """Main application class."""

    def __init__(self) -> None:
        """Initialize the application."""
        logger.debug("Initializing application")
        self.app = QApplication(sys.argv)

        # Timer threshold values
        self.MIN_WORK_DURATION: int = 25  # minimum work period duration
        self.MAX_WORK_DURATION: int = 60  # maximum work period duration
        self.BREAK_DURATION: int = 5  # break duration

        self.work_duration: int = self.MIN_WORK_DURATION
        self.work_duration_step: int = 5
        self.break_duration: int = self.BREAK_DURATION
        logger.debug(
            f"Set intervals: work={self.work_duration}m (min={self.MIN_WORK_DURATION}m, max={self.MAX_WORK_DURATION}m), "
            f"break={self.break_duration}m",
        )

        self.timer: QTimer = QTimer()
        self.timer.timeout.connect(self._on_timer_timeout)

        self.work_end_time: datetime | None = None
        self.break_end_time: datetime | None = None

        self.blocker = InputBlocker()
        self.overlay = BlockingOverlay()
        self.timer_widget = TimerWidget()

        # Initialize timer position
        self.current_position = TimerPosition.TOP_RIGHT
        self._update_timer_position()

        # Configure key handling
        self.overlay.keyPressEvent = self._handle_key_press
        
        # Configure global hotkeys (Alt+[1-4])
        keyboard.add_hotkey('alt+1', lambda: self._move_timer(TimerPosition.TOP_LEFT))
        keyboard.add_hotkey('alt+2', lambda: self._move_timer(TimerPosition.TOP_RIGHT))
        keyboard.add_hotkey('alt+3', lambda: self._move_timer(TimerPosition.BOTTOM_LEFT))
        keyboard.add_hotkey('alt+4', lambda: self._move_timer(TimerPosition.BOTTOM_RIGHT))

        # Show initial overlay
        self.show_initial_overlay()

        logger.info("Application initialized and ready to work")

    def _move_timer(self, position: TimerPosition) -> None:
        """Move timer to specified position."""
        self.current_position = position
        self._update_timer_position()
        logger.debug(f"Timer moved to {self.current_position.name}")

    def _update_timer_position(self) -> None:
        """Update timer widget position on screen."""
        if screen := self.app.primaryScreen():
            screen_geometry = screen.geometry()
            widget_size = self.timer_widget.size()

            match self.current_position:
                case TimerPosition.TOP_LEFT:
                    pos = QPoint(0, 0)
                case TimerPosition.TOP_RIGHT:
                    pos = QPoint(screen_geometry.width() - widget_size.width(), 0)
                case TimerPosition.BOTTOM_LEFT:
                    pos = QPoint(0, screen_geometry.height() - widget_size.height())
                case TimerPosition.BOTTOM_RIGHT:
                    pos = QPoint(screen_geometry.width() - widget_size.width(),
                               screen_geometry.height() - widget_size.height())

            self.timer_widget.move(pos)

    def show_initial_overlay(self) -> None:
        """Show initial overlay for time settings."""
        self.overlay.setText(
            f"Work time: {self.work_duration} minutes\n"
            f"Press:\n"
            f"↑/↓ to change time\n"
            f"Alt+[1-4] to move timer\n"
            f"Enter to start"
        )
        self.overlay.show()

    def _handle_key_press(self, a0: QKeyEvent | None) -> None:
        """Handle key presses."""
        if a0 is None:
            return
            
        key = a0.key()

        # Timer duration controls
        if key == Qt.Key.Key_Up:
            if self.work_duration < self.MAX_WORK_DURATION:
                self.work_duration += self.work_duration_step
                self.overlay.setText(
                    f"Work time: {self.work_duration} minutes\n"
                    f"Press:\n"
                    f"↑/↓ to change time\n"
                    f"Alt+[1-4] to move timer\n"
                    f"Enter to start"
                )
                logger.debug(f"Work time increased to {self.work_duration} minutes")
            else:
                logger.warning(f"Maximum work time limit reached ({self.MAX_WORK_DURATION} minutes)")

        elif key == Qt.Key.Key_Down:
            if self.work_duration > self.MIN_WORK_DURATION:
                self.work_duration -= self.work_duration_step
                self.overlay.setText(
                    f"Work time: {self.work_duration} minutes\n"
                    f"Press:\n"
                    f"↑/↓ to change time\n"
                    f"Alt+[1-4] to move timer\n"
                    f"Enter to start"
                )
                logger.debug(f"Work time decreased to {self.work_duration} minutes")
            else:
                logger.warning(f"Minimum work time limit reached ({self.MIN_WORK_DURATION} minutes)")

        elif key == Qt.Key.Key_Return:
            self.overlay.hide()
            self.start_work_timer()
            logger.info("Work timer started")

    def start_work_timer(self) -> None:
        """Start work timer."""
        if self.break_end_time is not None:
            logger.warning("Attempt to start timer during break")
            return

        self.work_end_time = datetime.now() + timedelta(minutes=self.work_duration)
        self.timer.start(1000)  # update every second
        self.timer_widget.show()
        self.blocker.unblock()  # Unblock input when work starts
        logger.info(f"Work timer started for {self.work_duration} minutes")

    def start_break_timer(self) -> None:
        """Start break timer."""
        self.break_end_time = datetime.now() + timedelta(minutes=self.break_duration)
        self.work_end_time = None
        self.blocker.block()  # Block input when break starts
        self.overlay.setText(f"Break: {self.break_duration} minutes")
        self.overlay.show()
        logger.info(f"Break started for {self.break_duration} minutes")

    def _on_timer_timeout(self) -> None:
        """Handle timer timeout."""
        now = datetime.now()

        if self.work_end_time:
            remaining = self.work_end_time - now
            if remaining.total_seconds() <= 0:
                logger.debug("Work time expired")
                self.start_break_timer()
            elif remaining.total_seconds() <= 60:
                logger.debug("One minute left until break")
                self.timer_widget.update_time(remaining)
            else:
                self.timer_widget.update_time(remaining)

        elif self.break_end_time:
            remaining = self.break_end_time - now
            if remaining.total_seconds() <= 0:
                logger.debug("Break time expired")
                self.end_break()
            else:
                self.overlay.update_time(remaining)

    def end_break(self) -> None:
        """End break."""
        self.break_end_time = None
        self.blocker.unblock()  # Unblock input when break ends
        self.overlay.hide()
        self.timer_widget.hide()
        self.timer.stop()
        self.show_initial_overlay()  # Show initial overlay again
        logger.info("Break ended")

    def quit(self) -> None:
        """Quit application."""
        if self.break_end_time is not None:
            logger.warning("Cannot quit during break")
            return
        self.blocker.unblock()
        self.app.quit()

    def run(self) -> int:
        """Run application."""
        return self.app.exec()
