"""Settings storage service for persistent data."""

from loguru import logger

from src.constants.settings import (
    AVAILABLE_WORK_MODES,
    DEFAULT_WORK_DURATION_MIN,
    LOAD_IMAGE_TIMEOUT_DEFAULT,
)
from src.db.db import Database
from src.schemas.settings import SettingsKey


class Settings:
    """Manages persistent settings storage using SQLite."""

    def __init__(self, db: Database) -> None:
        """Initialize the settings storage.

        Args:
            db: Database instance.

        """
        self.db = db
        self._ensure_defaults()

    def _ensure_defaults(self) -> None:
        """Ensure all default settings are present in database."""
        defaults = {
            SettingsKey.FOCUS: "",
            SettingsKey.FIRST_RUN_COMPLETE: "false",
            SettingsKey.USE_ONLINE_WALLPAPERS: "true",
            SettingsKey.WORK_DURATION: "45",
            SettingsKey.MOVE_TIMER_HOTKEY: "",
            SettingsKey.LOAD_IMAGE_TIMEOUT: str(LOAD_IMAGE_TIMEOUT_DEFAULT),
        }

        for key, value in defaults.items():
            if self.db.get(key) is None:
                self.db.set(key, value=value)

    def get_focus(self) -> str:
        """Get the saved focus text.

        Returns:
            The saved focus text or empty string.

        """
        return self.db.get(SettingsKey.FOCUS, "")

    def save_focus(self, focus: str) -> None:
        """Save the focus text.

        Args:
            focus: The focus text to save.

        """
        self.db.set(SettingsKey.FOCUS, value=focus)
        logger.debug(f"Focus saved: {focus}")

    def is_first_run(self) -> bool:
        """Check if this is the first run of the application.

        Returns:
            True if this is the first run, False otherwise.

        """
        return not self.db.get_bool(SettingsKey.FIRST_RUN_COMPLETE, default=False)

    def mark_first_run_complete(self) -> None:
        """Mark the first run as complete."""
        self.db.set(SettingsKey.FIRST_RUN_COMPLETE, value=True)
        logger.debug("First run marked as complete")

    def get_use_online_wallpapers(self) -> bool:
        """Get online wallpapers setting.

        Returns:
            Whether to use online wallpapers.

        """
        return self.db.get_bool(SettingsKey.USE_ONLINE_WALLPAPERS, default=True)

    def set_use_online_wallpapers(self, enabled: bool) -> None:
        """Set online wallpapers setting.

        Args:
            enabled: Whether to enable online wallpapers.

        """
        self.db.set(SettingsKey.USE_ONLINE_WALLPAPERS, value=enabled)
        logger.debug(f"Use online wallpapers set to: {enabled}")

    def get_work_duration(self) -> int:
        """Get work duration setting.

        Returns:
            Work duration in minutes (25 or 45).

        """
        return self.db.get_int(SettingsKey.WORK_DURATION, DEFAULT_WORK_DURATION_MIN)

    def set_work_duration(self, duration: int) -> None:
        """Set work duration setting.

        Args:
            duration: Work duration in minutes (should be 25 or 45).

        """
        if duration not in AVAILABLE_WORK_MODES:
            logger.warning(f"Invalid work duration: {duration}, using default: 45")
            duration = 45

        self.db.set(SettingsKey.WORK_DURATION, value=duration)
        logger.debug(f"Work duration set to: {duration} minutes")

    def get_move_timer_hotkey(self) -> str:
        """Get move timer hotkey setting.

        Returns:
            The saved move timer hotkey or empty string if not set.

        """
        return self.db.get(SettingsKey.MOVE_TIMER_HOTKEY, "")

    def set_move_timer_hotkey(self, hotkey: str) -> None:
        """Set move timer hotkey setting.

        Args:
            hotkey: The hotkey to save (e.g., "ctrl+alt+t").

        """
        self.db.set(SettingsKey.MOVE_TIMER_HOTKEY, value=hotkey)
        logger.debug(f"Move timer hotkey set to: {hotkey}")

    def get_load_image_timeout(self) -> int:
        """Get load image timeout setting.

        Returns:
            Load image timeout in seconds.

        """
        return self.db.get_int(SettingsKey.LOAD_IMAGE_TIMEOUT, LOAD_IMAGE_TIMEOUT_DEFAULT)

    def set_load_image_timeout(self, timeout: int) -> None:
        """Set load image timeout setting.

        Args:
            timeout: Load image timeout in seconds.

        """
        self.db.set(SettingsKey.LOAD_IMAGE_TIMEOUT, value=timeout)
        logger.debug(f"Load image timeout set to: {timeout} seconds")
