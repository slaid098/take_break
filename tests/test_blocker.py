"""Тесты для модуля блокировки ввода."""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Добавляем путь к пакету в PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

# Мокаем win32gui и win32con перед импортом InputBlocker
win32gui_mock = MagicMock()
win32con_mock = MagicMock()
win32con_mock.WH_KEYBOARD_LL = 13  # Реальное значение

with patch.dict('sys.modules', {'win32gui': win32gui_mock, 'win32con': win32con_mock}):
    from take_break.blocker import InputBlocker


class TestInputBlocker(unittest.TestCase):
    """Тесты для класса InputBlocker."""

    def setUp(self) -> None:
        """Подготовка к тестам."""
        self.blocker = InputBlocker()
        # Сбрасываем счетчики вызовов моков
        win32gui_mock.reset_mock()

    def test_block(self) -> None:
        """Тест блокировки ввода."""
        # Проверяем начальное состояние
        self.assertFalse(self.blocker._blocked)
        self.assertIsNone(self.blocker._hook_id)

        # Устанавливаем возвращаемое значение для SetWindowsHookEx
        win32gui_mock.SetWindowsHookEx.return_value = 123

        # Блокируем ввод
        self.blocker.block()

        # Проверяем, что хук был установлен
        self.assertTrue(self.blocker._blocked)
        self.assertEqual(self.blocker._hook_id, 123)
        win32gui_mock.SetWindowsHookEx.assert_called_once()

    def test_unblock(self) -> None:
        """Тест разблокировки ввода."""
        # Имитируем заблокированное состояние
        self.blocker._blocked = True
        self.blocker._hook_id = 123

        # Разблокируем ввод
        self.blocker.unblock()

        # Проверяем, что хук был удален
        self.assertFalse(self.blocker._blocked)
        self.assertIsNone(self.blocker._hook_id)
        win32gui_mock.UnhookWindowsHookEx.assert_called_once_with(123)

    def test_low_level_handler_blocked(self) -> None:
        """Тест обработчика событий в заблокированном состоянии."""
        self.blocker._blocked = True
        result = self.blocker._low_level_handler(1, 2, 3)
        self.assertEqual(result, 1)  # Все события блокируются
        win32gui_mock.CallNextHookEx.assert_not_called()

    def test_low_level_handler_unblocked(self) -> None:
        """Тест обработчика событий в разблокированном состоянии."""
        self.blocker._blocked = False
        self.blocker._hook_id = 123
        win32gui_mock.CallNextHookEx.return_value = 0

        result = self.blocker._low_level_handler(1, 2, 3)
        self.assertEqual(result, 0)
        win32gui_mock.CallNextHookEx.assert_called_once_with(123, 1, 2, 3)


if __name__ == '__main__':
    unittest.main()
