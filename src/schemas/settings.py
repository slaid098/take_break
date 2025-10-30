"""Settings keys enum for type safety and database storage."""

from enum import StrEnum


class SettingsKey(StrEnum):
    """Settings keys enum for type safety."""

    FOCUS = "focus"
    FIRST_RUN_COMPLETE = "first_run_complete"
    USE_ONLINE_WALLPAPERS = "use_online_wallpapers"
    WORK_DURATION = "work_duration"
    MOVE_TIMER_HOTKEY = "move_timer_hotkey"
    LOAD_IMAGE_TIMEOUT = "load_image_timeout"
