"""Tests for welcome dialog widget."""

from pytestqt.qtbot import QtBot

from src.constants.settings import POMODORO_MODE_MIN, STANDARD_MODE_MIN
from src.widgets.welcome import WelcomeDialog


def test_welcome_dialog_creation(qtbot: QtBot) -> None:
    """Test that welcome dialog is created successfully."""
    dialog = WelcomeDialog()
    qtbot.addWidget(dialog)

    assert dialog is not None
    assert dialog.windowTitle() == "Take Break"


def test_welcome_dialog_has_radio_buttons(qtbot: QtBot) -> None:
    """Test that welcome dialog has work mode radio buttons."""
    dialog = WelcomeDialog()
    qtbot.addWidget(dialog)

    # Radio buttons should exist
    assert dialog.radio_25 is not None
    assert dialog.radio_45 is not None

    # 45 minutes should be checked by default
    assert dialog.radio_45.isChecked()
    assert not dialog.radio_25.isChecked()


def test_welcome_dialog_default_selection(qtbot: QtBot) -> None:
    """Test that default work duration is 45 minutes."""
    dialog = WelcomeDialog()
    qtbot.addWidget(dialog)

    selected_duration = dialog.get_selected_work_duration()
    assert selected_duration == STANDARD_MODE_MIN


def test_welcome_dialog_select_25_minutes(qtbot: QtBot) -> None:
    """Test selecting 25 minutes (Pomodoro) mode."""
    dialog = WelcomeDialog()
    qtbot.addWidget(dialog)

    # Select 25 minutes
    dialog.radio_25.setChecked(True)

    selected_duration = dialog.get_selected_work_duration()
    assert selected_duration == POMODORO_MODE_MIN


def test_welcome_dialog_select_45_minutes(qtbot: QtBot) -> None:
    """Test selecting 45 minutes (Standard) mode."""
    dialog = WelcomeDialog()
    qtbot.addWidget(dialog)

    # Ensure 45 minutes is selected (should be default)
    dialog.radio_45.setChecked(True)

    selected_duration = dialog.get_selected_work_duration()
    assert selected_duration == STANDARD_MODE_MIN


def test_welcome_dialog_button_group(qtbot: QtBot) -> None:
    """Test that only one radio button can be selected at a time."""
    dialog = WelcomeDialog()
    qtbot.addWidget(dialog)

    # Both buttons should be in the same button group
    assert dialog.radio_25.group() == dialog.radio_45.group()
    assert dialog.radio_25.group() == dialog.work_mode_group


def test_welcome_dialog_switching_between_modes(qtbot: QtBot) -> None:
    """Test switching between 25 and 45 minute modes."""
    dialog = WelcomeDialog()
    qtbot.addWidget(dialog)

    # Start with 45 minutes (default)
    assert dialog.get_selected_work_duration() == STANDARD_MODE_MIN

    # Switch to 25 minutes
    dialog.radio_25.setChecked(True)
    assert dialog.get_selected_work_duration() == POMODORO_MODE_MIN

    # Switch back to 45 minutes
    dialog.radio_45.setChecked(True)
    assert dialog.get_selected_work_duration() == STANDARD_MODE_MIN

