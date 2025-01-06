"""Модуль блокировки ввода с клавиатуры и мыши."""

import win32con
import win32gui
from loguru import logger


class InputBlocker:
    """Класс для блокировки ввода с клавиатуры и мыши."""

    def __init__(self) -> None:
        """Инициализация блокировщика."""
        logger.debug("Инициализация блокировщика ввода")
        self._hook_id = None
        self._blocked = False

    def _low_level_handler(self, nCode: int, wParam: int, lParam: int) -> int:
        """Обработчик низкоуровневых событий Windows."""
        if self._blocked:
            logger.trace(f"Блокировка события: code={nCode}, wParam={wParam}")
            return 1  # блокируем все события
        return win32gui.CallNextHookEx(self._hook_id, nCode, wParam, lParam)

    def block(self) -> None:
        """Блокировка ввода."""
        if self._blocked:
            logger.debug("Попытка повторной блокировки ввода")
            return

        logger.debug("Установка хука для блокировки ввода")
        self._blocked = True
        try:
            # Устанавливаем хуки на клавиатуру и мышь
            self._hook_id = win32gui.SetWindowsHookEx(
                win32con.WH_KEYBOARD_LL,
                self._low_level_handler,
                None,
                0,
            )
            logger.info("Ввод заблокирован")
        except Exception as e:
            self._blocked = False
            logger.error(f"Ошибка при блокировке ввода: {e}")

    def unblock(self) -> None:
        """Разблокировка ввода."""
        if not self._blocked:
            logger.debug("Попытка разблокировки незаблокированного ввода")
            return

        logger.debug("Удаление хука блокировки")
        self._blocked = False
        if self._hook_id:
            try:
                win32gui.UnhookWindowsHookEx(self._hook_id)
                logger.info("Ввод разблокирован")
            except Exception as e:
                logger.error(f"Ошибка при разблокировке ввода: {e}")
            finally:
                self._hook_id = None
