"""Pytest configuration and fixtures."""

import pytest

from src.config.settings import Settings
from src.constants.path import Files
from src.db.db import Database


@pytest.fixture
def test_settings() -> Settings:
    """Get test settings instance."""
    db = Database(db_path=Files.MEMORY_DB_PATH)
    return Settings(db=db)
