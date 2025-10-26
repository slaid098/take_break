"""Settings storage service for persistent data."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

from loguru import logger

from src.config import settings


class SettingsDict(TypedDict, total=False):
    """Type definition for settings dictionary."""

    focus: str
    first_run_complete: bool
    use_online_wallpapers: bool
    work_duration: int
    move_timer_hotkey: str


@dataclass
class AppSettings:
    """Application settings model."""

    focus: str = ""
    first_run_complete: bool = False
    use_online_wallpapers: bool = True  # По умолчанию включено
    work_duration: int = 45  # По умолчанию 45 минут
    move_timer_hotkey: str = ""

    @classmethod
    def from_dict(cls, data: SettingsDict) -> "AppSettings":
        """Create AppSettings from dictionary.

        Args:
            data: Dictionary with settings.

        Returns:
            AppSettings instance.

        """
        return cls(
            focus=data.get("focus", ""),
            first_run_complete=data.get("first_run_complete", False),
            use_online_wallpapers=data.get("use_online_wallpapers", False),
            work_duration=data.get("work_duration", 45),
            move_timer_hotkey=data.get("move_timer_hotkey", ""),
        )

    def to_dict(self) -> SettingsDict:
        """Convert to dictionary.

        Returns:
            Dictionary with settings.

        """
        result: SettingsDict = {
            "focus": self.focus,
            "first_run_complete": self.first_run_complete,
            "use_online_wallpapers": self.use_online_wallpapers,
            "work_duration": self.work_duration,
        }
        if self.move_timer_hotkey:
            result["move_timer_hotkey"] = self.move_timer_hotkey
        return result


class SettingsStorage:
    """Manages persistent settings storage in JSON format."""

    def __init__(self, settings_dir: Path | None = None) -> None:
        """Initialize the settings storage.

        Args:
            settings_dir: Directory for settings. Defaults to APP_DATA_DIR/settings.

        """
        if settings_dir is None:
            settings_dir = settings.APP_DATA_DIR / "settings"
        self.settings_file = settings_dir / "settings.json"
        self._ensure_settings_dir_exists()

    def _ensure_settings_dir_exists(self) -> None:
        """Create settings directory if it doesn't exist."""
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)

    def _load_settings(self) -> AppSettings:
        """Load settings from JSON file.

        Returns:
            AppSettings instance with loaded settings or defaults.

        """
        if not self.settings_file.exists():
            return AppSettings()

        try:
            with self.settings_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return AppSettings.from_dict(data)
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Failed to load settings: {e}")
            return AppSettings()

    def _save_settings(self, app_settings: AppSettings) -> None:
        """Save settings to JSON file.

        Args:
            app_settings: AppSettings instance to save.

        """
        try:
            with self.settings_file.open("w", encoding="utf-8") as f:
                json.dump(app_settings.to_dict(), f, indent=2, ensure_ascii=False)
        except OSError as e:
            logger.error(f"Failed to save settings: {e}")

    def get_focus(self) -> str:
        """Get the saved focus text.

        Returns:
            The saved focus text or empty string.

        """
        settings_data = self._load_settings()
        return settings_data.focus

    def save_focus(self, focus: str) -> None:
        """Save the focus text.

        Args:
            focus: The focus text to save.

        """
        settings_data = self._load_settings()
        settings_data.focus = focus
        self._save_settings(settings_data)
        logger.debug(f"Focus saved: {focus}")

    def is_first_run(self) -> bool:
        """Check if this is the first run of the application.

        Returns:
            True if this is the first run, False otherwise.

        """
        settings_data = self._load_settings()
        return not settings_data.first_run_complete

    def mark_first_run_complete(self) -> None:
        """Mark the first run as complete."""
        settings_data = self._load_settings()
        settings_data.first_run_complete = True
        self._save_settings(settings_data)
        logger.debug("First run marked as complete")

    def get_use_online_wallpapers(self) -> bool:
        """Get online wallpapers setting.

        Returns:
            Whether to use online wallpapers.

        """
        settings_data = self._load_settings()
        return settings_data.use_online_wallpapers

    def set_use_online_wallpapers(self, enabled: bool) -> None:
        """Set online wallpapers setting.

        Args:
            enabled: Whether to enable online wallpapers.

        """
        settings_data = self._load_settings()
        settings_data.use_online_wallpapers = enabled
        self._save_settings(settings_data)
        logger.debug(f"Use online wallpapers set to: {enabled}")

    def get_work_duration(self) -> int:
        """Get work duration setting.

        Returns:
            Work duration in minutes (25 or 45).

        """
        settings_data = self._load_settings()
        return settings_data.work_duration

    def set_work_duration(self, duration: int) -> None:
        """Set work duration setting.

        Args:
            duration: Work duration in minutes (should be 25 or 45).

        """
        if duration not in settings.AVAILABLE_WORK_MODES:
            logger.warning(f"Invalid work duration: {duration}, using default: 45")
            duration = 45

        settings_data = self._load_settings()
        settings_data.work_duration = duration
        self._save_settings(settings_data)
        logger.debug(f"Work duration set to: {duration} minutes")

    def get_move_timer_hotkey(self) -> str:
        """Get move timer hotkey setting.

        Returns:
            The saved move timer hotkey or empty string if not set.

        """
        settings_data = self._load_settings()
        return settings_data.move_timer_hotkey

    def set_move_timer_hotkey(self, hotkey: str) -> None:
        """Set move timer hotkey setting.

        Args:
            hotkey: The hotkey to save (e.g., "ctrl+alt+t").

        """
        settings_data = self._load_settings()
        settings_data.move_timer_hotkey = hotkey
        self._save_settings(settings_data)
        logger.debug(f"Move timer hotkey set to: {hotkey}")

