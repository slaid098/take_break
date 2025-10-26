"""Pytest configuration and fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def temp_settings_dir(tmp_path: Path) -> Path:
    """Temporary directory for settings tests."""
    return tmp_path / "settings"
