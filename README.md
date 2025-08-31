# MAX Bot Library

Сервис для создания ботов в приложении MAX с поддержкой асинхронных методов и модульной архитектуры.

## Особенности

- 🚀 Асинхронная архитектура
- 🧩 Модульная структура
- 🔧 Система фильтров и middleware
- 📝 Типизация данных
- 🎯 Простой и понятный API
- 🤖 Встроенный конструктор ботов
- 🔗 Интеграция с MAX API
- ✅ Полное тестирование

## Установка

```bash
git clone https://github.com/Moskvafm/Max_bot.git
cd Max_bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Быстрый старт

### Простой бот

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

### Бот-конструктор

```python
from constructor.dialog.constructor_bot import ConstructorBot

# Создаем бота-конструктор
constructor = ConstructorBot("YOUR_CONSTRUCTOR_TOKEN")
constructor.run()
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
    └── http_client.py

constructor/        # Конструктор ботов
├── dialog/         # Диалоговый интерфейс
├── templates/      # Шаблоны
└── generator/      # Генератор кода

examples/           # Примеры использования
templates/          # Шаблоны ботов
tests/              # Тесты
```

## API Документация

### Основные классы

#### Dispatcher
Основной класс для управления ботом.

```python
dp = Dispatcher("YOUR_TOKEN")
dp.run()
```

#### Router
Организация обработчиков.

```python
router = Router("my_router")
dp.include_router(router)
```

#### Фильтры
```python
from max_bot.filters.base import command, text, callback_data

@dp.message_handler(command("start"))
async def start_handler(message):
    pass

@dp.message_handler(text("привет"))
async def hello_handler(message):
    pass
```

#### Middleware
```python
from max_bot.middleware.base import LoggingMiddleware

dp.add_middleware(LoggingMiddleware())
```

### Конструктор ботов

#### Доступные шаблоны
1. **Простой бот** - базовые команды
2. **Эхо-бот** - повторение сообщений
3. **FAQ бот** - часто задаваемые вопросы
4. **Магазин бот** - интернет-магазин
5. **Кастомный бот** - настраиваемый

#### Команды конструктора
- `/start` - Начать работу
- `/create` - Создать нового бота
- `/help` - Справка
- `/cancel` - Отменить создание
- `/status` - Статус создания

## Тестирование

```bash
# Запуск всех тестов
pytest

# Запуск конкретного теста
pytest tests/test_basic.py::TestTypes::test_user_creation

# Запуск с покрытием
pytest --cov=max_bot
```

## Разработка

### Установка зависимостей для разработки
```bash
pip install -r requirements.txt
```

### Форматирование кода
```bash
black max_bot/ constructor/ tests/
```

### Проверка типов
```bash
mypy max_bot/ constructor/
```

### Линтинг
```bash
flake8 max_bot/ constructor/ tests/
```

## Примеры

Смотрите папку `examples/` для примеров использования библиотеки:

- `simple_bot.py` - Простой бот
- `constructor_bot.py` - Бот-конструктор

## Лицензия

MIT License

## Автор

Создано с помощью MAX Bot Constructor
