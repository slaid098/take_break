"""SQLite хранилище настроек в формате ключ-значение."""

import contextlib
import sqlite3
from pathlib import Path

from loguru import logger

from src.constants.path import Files


class Database:
    """SQLite база данных в формате ключ-значение."""

    def __init__(self, db_path: Path | str | None = None) -> None:
        """Инициализировать базу данных.

        Args:
            db_path: Путь к файлу базы данных.
                    По умолчанию использует Files.SETTINGS_DB_PATH.
                    Передайте ":memory:" для in-memory базы (тесты).

        """
        if db_path is None:
            db_path = Files.SETTINGS_DB_PATH
        self.db_path = db_path
        if str(db_path) != ":memory:":
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._connection: sqlite3.Connection = sqlite3.connect(
            str(db_path),
            check_same_thread=False,
        )
        self._init_db()

    def _init_db(self) -> None:
        """Создать таблицу настроек если не существует."""
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """,
        )
        self._connection.commit()

    def get(self, key: str, default: str | None = None) -> str | None:
        """Получить значение настройки.

        Args:
            key: Ключ настройки.
            default: Значение по умолчанию если ключ не найден.

        Returns:
            Значение настройки или default.

        """
        result = self._connection.execute(
            "SELECT value FROM settings WHERE key=?",
            (key,),
        ).fetchone()
        return result[0] if result else default

    def set(self, key: str, value: str | int | bool) -> None:
        """Установить значение настройки.

        Args:
            key: Ключ настройки.
            value: Значение (будет преобразовано в строку).

        """
        self._connection.execute(
            """
            INSERT INTO settings (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
            """,
            (key, str(value)),
        )
        self._connection.commit()

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Получить булево значение настройки.

        Args:
            key: Ключ настройки.
            default: Значение по умолчанию.

        Returns:
            Булево значение.

        """
        value = self.get(key)
        if value is None:
            return default
        return value.lower() == "true"

    def get_int(self, key: str, default: int = 0) -> int:
        """Получить целочисленное значение настройки.

        Args:
            key: Ключ настройки.
            default: Значение по умолчанию.

        Returns:
            Целочисленное значение.

        """
        value = self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError) as e:
            logger.warning(f"Не удалось преобразовать '{key}' в int: {e}")
            return default

    def close(self) -> None:
        """Закрыть соединение с базой данных."""
        self._connection.close()

    def __enter__(self) -> "Database":
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.close()

    def __del__(self) -> None:
        """Закрыть соединение при уничтожении объекта."""
        with contextlib.suppress(sqlite3.ProgrammingError):
            self._connection.close()
