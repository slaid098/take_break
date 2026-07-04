<div align="center">
  <img src="https://github.com/slaid098/take_break/blob/master/images/logo.png?raw=true" alt="Take Break" width="100"/>
  <h1>Take Break</h1>
  <p><strong>Циклический таймер для эффективной работы и отдыха за ПК.</strong></p>
  <p>
    <img src="https://img.shields.io/badge/ОС-Windows-blue" alt="Windows">
  </p>
  <p><a href="https://github.com/slaid098/take_break/releases"><strong>Скачать</strong></a></p>
</div>

---

![Take Break Demo](https://github.com/slaid098/take_break/blob/master/images/demo.gif?raw=true)
*Приветствие → Фокус → Работа → Перерыв → Возврат к фокусу.*

---

## Возможности

- Фиксированные интервалы работы, гибкий отдых
- Два режима: Помодоро (25 мин) и Стандартный (45 мин)
- Перерыв пропустить нельзя
- Онлайн-обои при каждом перерыве
- Автозапуск с Windows

## Установка

Портативное приложение для **Windows 10+**. Не требует установки.

1. Скачайте `take_break.zip` со страницы [**Releases**](https://github.com/slaid098/take_break/releases).
2. Распакуйте в любую папку.
3. Запустите `take_break.exe`.

<details>
<summary><strong>Для разработчиков</strong></summary>

Управляется через [uv](https://github.com/astral-sh/uv). Python 3.13+.

```bash
git clone https://github.com/slaid098/take_break
cd take_break
uv sync --group dev
uv run python main.py
```

Тесты и проверки:

```bash
QT_QPA_PLATFORM=offscreen uv run pytest
uv run ruff check src/ tests/
uv run mypy src/
```

</details>

## Лицензия

[MIT](LICENSE) © 2024-2025 slaid098