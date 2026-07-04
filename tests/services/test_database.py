"""Тесты базы данных настроек."""

import pytest
from src.constants.path import Files
from src.db.db import Database


class TestDatabase:
    """Тесты SQLite хранилища ключ-значение."""

    @pytest.fixture
    def db(self) -> Database:
        """Создать in-memory базу данных."""
        return Database(db_path=Files.MEMORY_DB_PATH)

    def test_get_returns_none_for_missing_key(self, db: Database) -> None:
        """get возвращает None для несуществующего ключа."""
        assert db.get("nonexistent") is None

    def test_get_returns_default_for_missing_key(self, db: Database) -> None:
        """get возвращает default для несуществующего ключа."""
        assert db.get("nonexistent", "fallback") == "fallback"

    def test_set_and_get_roundtrip(self, db: Database) -> None:
        """set и get работают корректно."""
        db.set("test_key", "test_value")
        assert db.get("test_key") == "test_value"

    def test_set_overwrites_existing_value(self, db: Database) -> None:
        """set перезаписывает существующее значение."""
        db.set("key", "value1")
        db.set("key", "value2")
        assert db.get("key") == "value2"

    def test_set_converts_int_to_string(self, db: Database) -> None:
        """set преобразует int в строку."""
        db.set("number", 42)
        assert db.get("number") == "42"

    def test_set_converts_bool_to_string(self, db: Database) -> None:
        """set преобразует bool в строку."""
        db.set("flag", True)
        assert db.get("flag") == "True"

    def test_get_bool_returns_true_for_true_string(self, db: Database) -> None:
        """get_bool возвращает True для строки 'true'."""
        db.set("flag", "true")
        assert db.get_bool("flag") is True

    def test_get_bool_returns_false_for_false_string(self, db: Database) -> None:
        """get_bool возвращает False для строки 'false'."""
        db.set("flag", "false")
        assert db.get_bool("flag") is False

    def test_get_bool_returns_default_for_missing_key(self, db: Database) -> None:
        """get_bool возвращает default для несуществующего ключа."""
        assert db.get_bool("missing", default=True) is True
        assert db.get_bool("missing", default=False) is False

    def test_get_int_returns_int_value(self, db: Database) -> None:
        """get_int возвращает int значение."""
        db.set("number", "123")
        assert db.get_int("number") == 123

    def test_get_int_returns_default_for_missing_key(self, db: Database) -> None:
        """get_int возвращает default для несуществующего ключа."""
        assert db.get_int("missing", default=99) == 99

    def test_get_int_returns_default_for_invalid_value(self, db: Database) -> None:
        """get_int возвращает default для некорректного значения."""
        db.set("bad", "not_a_number")
        assert db.get_int("bad", default=0) == 0

    def test_context_manager_closes_connection(self) -> None:
        """Context manager закрывает соединение."""
        with Database(db_path=Files.MEMORY_DB_PATH) as db:
            db.set("key", "value")
            assert db.get("key") == "value"

    def test_close_connection(self, db: Database) -> None:
        """close закрывает соединение без ошибок."""
        db.set("key", "value")
        db.close()
