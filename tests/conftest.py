"""Конфигурация для тестов."""

import sys
from pathlib import Path

# Добавляем путь к пакету в PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

# Отключаем логирование во время тестов
from loguru import logger

logger.remove()  # Удаляем все обработчики
logger.add(sys.stderr, level="ERROR")  # Добавляем только критические ошибки
