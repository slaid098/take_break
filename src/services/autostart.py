"""Windows autostart management service."""

import sys
import winreg
from pathlib import Path

from loguru import logger


def get_exe_path() -> str | None:
    """Get the path to the executable if running as compiled exe.

    Returns:
        The absolute path to the .exe file, or None if running from Python script.

    """
    # Check if running as compiled executable (PyInstaller sets sys.frozen)
    if not getattr(sys, "frozen", False):
        return None

    # sys.executable will be the .exe path when frozen
    return str(Path(sys.executable).resolve())


def is_autostart_enabled() -> bool:
    """Check if autostart is currently enabled in Windows registry.

    Returns:
        True if autostart is enabled, False otherwise.

    """
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
        )
        try:
            winreg.QueryValueEx(key, "TakeBreak")
        except FileNotFoundError:
            return False
        else:
            return True
        finally:
            winreg.CloseKey(key)
    except Exception as e:
        logger.error(f"Failed to check autostart status: {e}")
        return False


def enable_autostart() -> None:
    r"""Enable autostart by adding TakeBreak to Windows registry.

    Adds an entry to HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
    that runs the application executable.
    """
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE,
        )
        try:
            exe_path = get_exe_path()
            winreg.SetValueEx(key, "TakeBreak", 0, winreg.REG_SZ, exe_path)
            logger.info("Autostart enabled")
        finally:
            winreg.CloseKey(key)
    except Exception as e:
        logger.error(f"Failed to enable autostart: {e}")


def disable_autostart() -> None:
    """Disable autostart by removing TakeBreak from Windows registry."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE,
        )
        winreg.DeleteValue(key, "TakeBreak")
        winreg.CloseKey(key)
        logger.info("Autostart disabled")
    except FileNotFoundError:
        logger.debug("Autostart entry not found, nothing to remove")
    except Exception as e:
        logger.error(f"Failed to disable autostart: {e}")

