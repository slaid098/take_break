"""Скрипт для создания иконки приложения."""

from pathlib import Path

from PIL import Image, ImageDraw

# Создаем новое изображение с прозрачным фоном
size = (256, 256)
image = Image.new('RGBA', size, (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# Рисуем круг (циферблат)
margin = 20
circle_bbox = (margin, margin, size[0] - margin, size[1] - margin)
draw.ellipse(circle_bbox, outline=(0, 120, 215), width=10)

# Рисуем стрелки
center = (size[0] // 2, size[1] // 2)
# Часовая стрелка (45 градусов)
draw.line(
    (center[0], center[1], center[0] + 60, center[1] - 60),
    fill=(0, 120, 215),
    width=10,
)
# Минутная стрелка (вертикально вверх)
draw.line(
    (center[0], center[1], center[0], center[1] - 90),
    fill=(0, 120, 215),
    width=10,
)

# Сохраняем как .ico
image.save(Path(__file__).parent / 'icon.ico', format='ICO', sizes=[(256, 256)]) 