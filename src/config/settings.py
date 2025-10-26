"""Module for application settings."""

from pathlib import Path

# --- Paths ---
APP_NAME = "TakeBreak"
APP_DATA_DIR = Path("app_data")
LOGS_DIR = APP_DATA_DIR / "logs"
WALLPAPERS_DIR = APP_DATA_DIR / "wallpapers"
CACHE_DIR = APP_DATA_DIR / "cache"
ICON_PATH = APP_DATA_DIR / "icon" / "icon.ico"
WALLPAPER_CACHE_PATH = CACHE_DIR / "wallpaper_cache.jpg"


def ensure_dirs_exist() -> None:
    """Create all necessary application directories."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    WALLPAPERS_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    ICON_PATH.parent.mkdir(parents=True, exist_ok=True)


# --- Durations ---
POMODORO_MODE_MIN = 25
STANDARD_MODE_MIN = 45
DEFAULT_WORK_DURATION_MIN = STANDARD_MODE_MIN
AVAILABLE_WORK_MODES = [POMODORO_MODE_MIN, STANDARD_MODE_MIN]
BREAK_DURATION_MIN = 5
TIMER_INTERVAL_MS = 1000

# --- Hotkeys ---
MOVE_TIMER_HOTKEY = "ctrl+alt+t"

# --- UI Options ---
MAX_FOCUS_LENGTH = 50
RED_SECOND_THRESHOLD = 60


# --- Screen Dimensions ---
PRELOAD_WIDTH_DEFAULT = 1920
PRELOAD_HEIGHT_DEFAULT = 1080
