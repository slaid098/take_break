# AGENTS.md

## Правила работы
- Каждый важный факт сразу сохранять в память (`memory_save`)
- Перед ответом ищи релевантный контекст (memory_search)
- Если информации не хватает — спрашивай, а не додумывай
- При сжатии (compaction) сохраняй ключевые решения и discoveries

## Стандарты кода
- Python 3.13+, строгая типизация (mypy strict)
- Ruff для линтинга и форматирования
- Все UI-тексты и логи на русском языке
- Docstrings на русском
- Тесты: pytest + pytest-qt (QT_QPA_PLATFORM=offscreen на CI)
- Coverage порог: 60%

## Команды
- `uv sync --group dev` — установить зависимости
- `uv run python main.py` — запустить приложение
- `QT_QPA_PLATFORM=offscreen uv run pytest` — запустить тесты
- `uv run ruff check src/ tests/` — линтер
- `uv run ruff format src/ tests/` — форматирование
- `uv run mypy src/` — проверка типов

## Структура
- `src/constants/` — константы (пути, настройки, URL)
- `src/config/` — конфигурация (логгер, настройки, тексты)
- `src/services/` — бизнес-логика (таймер, позиции, обои, автозапуск)
- `src/widgets/` — Qt виджеты (overlay, таймер, трей, welcome)
- `src/db/` — SQLite хранилище настроек
- `src/schemas/` — типы и enum'ы
- `src/utils/` — утилиты (форматирование времени)
- `tests/` — тесты (pytest + pytest-qt)