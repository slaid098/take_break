"""SQLite-based Key-Value settings storage service."""

import sqlite3
from pathlib import Path
from typing import Any

from loguru import logger

from src.constants.path import Files


class Database:
    """SQLite-based Key-Value database."""

    def __init__(self, db_path: Path | str | None = None) -> None:
        """Initialize the database.

        Args:
            db_path: Path to database file. Defaults to settings.SETTINGS_DIR/settings.db.

        """
        self._connection: sqlite3.Connection | None = None
        if db_path is None:
            db_path = Files.SETTINGS_DB_PATH
        if db_path == Files.MEMORY_DB_PATH:
            self._connection = sqlite3.connect(db_path)
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Create table if not exists."""
        command = """
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
        if self._connection:
            self._connection.execute(command)
            self._connection.commit()
        else:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(command)
                conn.commit()

    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value.

        Args:
            key: Setting key.
            default: Default value if key not found.

        Returns:
            Setting value or default.

        """
        command = "SELECT value FROM settings WHERE key=?"
        if self._connection:
            result = self._connection.execute(command, (key,)).fetchone()
            return result[0] if result else default

        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute(command, (key,)).fetchone()
            return result[0] if result else default

    def set(self, key: str, value: Any) -> None:
        """Set setting value.

        Args:
            key: Setting key.
            value: Setting value (will be converted to string).

        """
        command = """
        INSERT INTO settings (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """
        if self._connection:
            self._connection.execute(command, (key, str(value)))
            self._connection.commit()
        else:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(command, (key, str(value)))

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean setting.

        Args:
            key: Setting key.
            default: Default value if key not found.

        Returns:
            Boolean setting value.

        """
        value = self.get(key)
        if value is None:
            return default
        return str(value).lower() == "true"

    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer setting.

        Args:
            key: Setting key.
            default: Default value if key not found.

        Returns:
            Integer setting value.

        """
        value = self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError) as e:
            logger.warning(f"Failed to convert setting '{key}' to int: {e}")
            return default

    def __del__(self) -> None:
        """Close connection on object destruction."""
        if self._connection:
            self._connection.close()
