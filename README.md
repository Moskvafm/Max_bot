# MAX Bot Library

Аналог aiogram для создания ботов в приложении MAX с поддержкой асинхронных методов и модульной архитектуры.

## Особенности

- 🚀 Асинхронная архитектура
- 🧩 Модульная структура
- 🔧 Система фильтров и middleware
- 📝 Типизация данных
- 🎯 Простой и понятный API

## Установка

```bash
git clone https://github.com/Moskvafm/Max_bot.git
cd Max_bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Быстрый старт

```python
from max_bot import Dispatcher
from max_bot.filters.base import command

# Создаем диспетчер
dp = Dispatcher("YOUR_BOT_TOKEN")

@dp.message_handler(command("start"))
async def start_command(message):
    await message.answer("Привет! Я бот!")

# Запускаем бота
dp.run()
```

## Структура проекта

```
max_bot/
├── core/           # Основные классы
│   ├── dispatcher.py
│   ├── router.py
│   ├── handler.py
│   └── types.py
├── filters/        # Фильтры
│   └── base.py
├── middleware/     # Промежуточное ПО
│   └── base.py
└── utils/          # Утилиты

constructor/        # Конструктор ботов
├── dialog/         # Диалоговый интерфейс
├── templates/      # Шаблоны
└── generator/      # Генератор кода

examples/           # Примеры использования
templates/          # Шаблоны ботов
tests/              # Тесты
```

## Примеры

Смотрите папку `examples/` для примеров использования библиотеки.

## Лицензия

MIT License
