<div align="center">
  <img src="https://github.com/slaid098/take_break/blob/master/images/logo.png?raw=true" alt="Take Break Logo" width="100"/>
  <h1>Take Break</h1>
  <p><strong>Простой неотключаемый таймер перерывов для защиты здоровья и фокуса.</strong></p>
  <p><i>Дисциплина в работе, свобода в отдыхе.</i></p>
  <p>
    <img src="https://img.shields.io/badge/ОС-Windows-blue" alt="Windows OS">
  </p>
  <p><a href="https://github.com/slaid098/take_break/releases"><strong>Скачать последнюю версию для Windows</strong></a></p>
</div>

---

![Take Break Demo](https://github.com/slaid098/take_break/blob/master/images/demo.gif?raw=true)
*Основной цикл: Приветствие → Фокус → Работа → Обязательный перерыв → Возврат к фокусу.*

---

## Возможности

- Устанавливайте фокус на следующую рабочую сессию.
- **Работайте фиксированное время, отдыхайте сколько нужно.**
- Новые фоновые обои при каждом перерыве.
- Выйти из приложения можно только во время рабочей сессии.
- Два режима: 45 минут (Стандартный) или 25 минут (Помодоро).
- Полноэкранный overlay, блокирующий отвлекающие факторы.

## Установка и запуск

Приложение **портативное** и не требует установки.
**Доступно для Windows 10 и новее.**

1. Перейдите на страницу [**Releases**](https://github.com/slaid098/take_break/releases).
2. Скачайте `take_break_vX.X.zip` (или последнюю версию).
3. Распакуйте папку в удобное место.
4. Запустите `take_break.exe`.

<details>
<summary><strong>Запуск из исходного кода (для разработчиков)</strong></summary>

Проект управляется через [uv](https://github.com/astral-sh/uv).

**Требования:**
- Python 3.13+
- `uv` установлен

**Шаги:**

1. **Клонировать репозиторий:**
   ```bash
   git clone https://github.com/slaid098/take_break
   cd take_break
   ```

2. **Синхронизировать окружение и установить зависимости:**
   ```bash
   uv sync --group dev
   ```

3. **Запустить приложение:**
   ```bash
   uv run python main.py
   ```

4. **Запустить тесты:**
   ```bash
   QT_QPA_PLATFORM=offscreen uv run pytest
   ```

5. **Проверить типы и линтер:**
   ```bash
   uv run mypy src/
   uv run ruff check src/ tests/
   ```

</details>

## Лицензия

[MIT](LICENSE) © 2024-2025 slaid098