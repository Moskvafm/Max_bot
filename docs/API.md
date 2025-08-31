# MAX Bot Library API Documentation

## Содержание

1. [Основные концепции](#основные-концепции)
2. [Dispatcher](#dispatcher)
3. [Router](#router)
4. [Handlers](#handlers)
5. [Filters](#filters)
6. [Middleware](#middleware)
7. [Types](#types)
8. [HTTP Client](#http-client)
9. [Constructor](#constructor)

## Основные концепции

MAX Bot Library - это асинхронная библиотека для создания ботов в приложении MAX, вдохновленная aiogram.

### Архитектура

```
Dispatcher (главный класс)
├── Router (организация обработчиков)
├── Handlers (обработчики сообщений)
├── Filters (фильтрация сообщений)
├── Middleware (промежуточное ПО)
└── HTTP Client (работа с API)
```

## Dispatcher

Основной класс для управления ботом.

### Инициализация

```python
from max_bot import Dispatcher

dp = Dispatcher("YOUR_BOT_TOKEN")
```

### Методы

#### `run(token: str = None)`
Запуск бота с polling.

```python
dp.run()  # Использует токен из инициализации
dp.run("NEW_TOKEN")  # Использует новый токен
```

#### `start_polling(timeout: int = 30, limit: int = 100)`
Асинхронный запуск polling.

```python
await dp.start_polling()
```

#### `stop_polling()`
Остановка polling.

```python
dp.stop_polling()
```

#### `process_update(update: Update)`
Обработка одного обновления.

```python
result = await dp.process_update(update)
```

#### `include_router(router: Router)`
Включение роутера.

```python
router = Router("my_router")
dp.include_router(router)
```

#### `add_middleware(middleware: BaseMiddleware)`
Добавление middleware.

```python
from max_bot.middleware.base import LoggingMiddleware
dp.add_middleware(LoggingMiddleware())
```

### Декораторы

#### `@dp.message_handler(filters=None)`
Регистрация обработчика сообщений.

```python
@dp.message_handler(command("start"))
async def start_handler(message):
    await message.answer("Привет!")
```

#### `@dp.callback_query_handler(filters=None)`
Регистрация обработчика callback запросов.

```python
@dp.callback_query_handler(callback_data("button"))
async def button_handler(callback_query):
    await callback_query.answer("Кнопка нажата!")
```

## Router

Организация обработчиков в модули.

### Инициализация

```python
from max_bot.core.router import Router

router = Router("my_router")
```

### Методы

#### `message_handler(filters=None)`
Декоратор для обработчиков сообщений.

```python
@router.message_handler(command("help"))
async def help_handler(message):
    await message.answer("Справка")
```

#### `callback_query_handler(filters=None)`
Декоратор для обработчиков callback.

```python
@router.callback_query_handler(callback_data("menu"))
async def menu_handler(callback_query):
    await callback_query.answer("Меню")
```

#### `include_router(other_router: Router)`
Включение другого роутера.

```python
admin_router = Router("admin")
user_router = Router("user")
main_router.include_router(admin_router)
main_router.include_router(user_router)
```

#### `add_handler(handler: Handler)`
Добавление обработчика напрямую.

```python
from max_bot.core.handler import MessageHandler
handler = MessageHandler(my_function)
router.add_handler(handler)
```

## Handlers

Обработчики сообщений и событий.

### MessageHandler

Обработчик сообщений.

```python
from max_bot.core.handler import MessageHandler

async def my_handler(message):
    await message.answer("Ответ")

handler = MessageHandler(my_handler, filters=command("start"))
```

### CallbackQueryHandler

Обработчик callback запросов.

```python
from max_bot.core.handler import CallbackQueryHandler

async def my_callback_handler(callback_query):
    await callback_query.answer("OK")

handler = CallbackQueryHandler(my_callback_handler, filters=callback_data("button"))
```

### Декораторы

#### `@message_handler(filters=None)`
Удобный декоратор для обработчиков сообщений.

```python
from max_bot.core.handler import message_handler

@message_handler(command("start"))
async def start_handler(message):
    await message.answer("Старт")
```

#### `@callback_query_handler(filters=None)`
Удобный декоратор для обработчиков callback.

```python
from max_bot.core.handler import callback_query_handler

@callback_query_handler(callback_data("menu"))
async def menu_handler(callback_query):
    await callback_query.answer("Меню")
```

## Filters

Фильтрация сообщений и событий.

### Доступные фильтры

#### TextFilter
Фильтр по тексту сообщения.

```python
from max_bot.filters.base import text

@dp.message_handler(text("привет"))
async def hello_handler(message):
    await message.answer("Привет!")

# Несколько вариантов
@dp.message_handler(text(["привет", "hello", "hi"]))
async def hello_handler(message):
    await message.answer("Привет!")
```

#### CommandFilter
Фильтр по командам.

```python
from max_bot.filters.base import command

@dp.message_handler(command("start"))
async def start_handler(message):
    await message.answer("Старт")

# Несколько команд
@dp.message_handler(command(["start", "help"]))
async def command_handler(message):
    await message.answer("Команда")
```

#### CallbackDataFilter
Фильтр по данным callback.

```python
from max_bot.filters.base import callback_data

@dp.callback_query_handler(callback_data("button"))
async def button_handler(callback_query):
    await callback_query.answer("Кнопка")

# Несколько вариантов
@dp.callback_query_handler(callback_data(["button1", "button2"]))
async def button_handler(callback_query):
    await callback_query.answer("Кнопка")
```

#### ChatTypeFilter
Фильтр по типу чата.

```python
from max_bot.filters.base import chat_type

@dp.message_handler(chat_type("private"))
async def private_handler(message):
    await message.answer("Приватный чат")

@dp.message_handler(chat_type(["group", "supergroup"]))
async def group_handler(message):
    await message.answer("Групповой чат")
```

#### UserFilter
Фильтр по пользователю.

```python
from max_bot.filters.base import user

@dp.message_handler(user(123456789))
async def admin_handler(message):
    await message.answer("Админ")

@dp.message_handler(user([123456789, 987654321]))
async def admin_handler(message):
    await message.answer("Админ")
```

### Комбинирование фильтров

```python
from max_bot.filters.base import command, chat_type

# Логическое И (все фильтры должны сработать)
@dp.message_handler(command("admin"), chat_type("private"), user(123456789))
async def admin_handler(message):
    await message.answer("Админ команда")
```

## Middleware

Промежуточное ПО для обработки запросов.

### Встроенные middleware

#### LoggingMiddleware
Логирование запросов.

```python
from max_bot.middleware.base import LoggingMiddleware
import logging

logger = logging.getLogger(__name__)
dp.add_middleware(LoggingMiddleware(logger))
```

#### ThrottlingMiddleware
Ограничение частоты запросов.

```python
from max_bot.middleware.base import ThrottlingMiddleware

# 1 запрос в секунду
dp.add_middleware(ThrottlingMiddleware(rate_limit=1.0))

# 2 запроса в секунду
dp.add_middleware(ThrottlingMiddleware(rate_limit=0.5))
```

#### ErrorHandlingMiddleware
Обработка ошибок.

```python
from max_bot.middleware.base import ErrorHandlingMiddleware

async def error_handler(exception, update):
    print(f"Ошибка: {exception}")
    return "Ошибка обработана"

dp.add_middleware(ErrorHandlingMiddleware(error_handler))
```

### Создание собственного middleware

```python
from max_bot.middleware.base import BaseMiddleware

class MyMiddleware(BaseMiddleware):
    async def __call__(self, handler, update):
        print(f"Обработка обновления {update.update_id}")
        result = await handler(update)
        print(f"Обновление {update.update_id} обработано")
        return result

dp.add_middleware(MyMiddleware())
```

## Types

Типы данных для работы с MAX API.

### User
Пользователь.

```python
from max_bot.core.types import User

user = User(
    id=123456789,
    username="username",
    first_name="Имя",
    last_name="Фамилия",
    is_bot=False
)
```

### Chat
Чат.

```python
from max_bot.core.types import Chat

chat = Chat(
    id=123456789,
    type="private",  # private, group, supergroup, channel
    title="Название чата",
    username="chat_username"
)
```

### Message
Сообщение.

```python
from max_bot.core.types import Message
from datetime import datetime

message = Message(
    message_id=1,
    date=datetime.now(),
    chat=chat,
    from_user=user,
    text="Текст сообщения",
    caption="Подпись",
    reply_to_message=None,
    entities=[]
)

# Ответ на сообщение
await message.answer("Ответ")
```

### CallbackQuery
Callback запрос.

```python
from max_bot.core.types import CallbackQuery

callback_query = CallbackQuery(
    id="callback_id",
    from_user=user,
    message=message,
    data="callback_data"
)

# Ответ на callback
await callback_query.answer("Ответ")
```

### Update
Обновление от API.

```python
from max_bot.core.types import Update

update = Update(
    update_id=1,
    message=message,
    callback_query=callback_query,
    edited_message=None,
    channel_post=None,
    edited_channel_post=None
)
```

## HTTP Client

Клиент для работы с MAX API.

### Инициализация

```python
from max_bot.utils.http_client import MaxAPIClient

async with MaxAPIClient("YOUR_TOKEN") as client:
    # Работа с API
    pass
```

### Методы

#### `get_me()`
Получение информации о боте.

```python
bot_info = await client.get_me()
print(f"Bot: @{bot_info.username}")
```

#### `get_updates(offset=None, limit=100)`
Получение обновлений.

```python
updates = await client.get_updates(offset=0, limit=10)
for update in updates:
    print(f"Update ID: {update.update_id}")
```

#### `send_message(chat_id, text, **kwargs)`
Отправка сообщения.

```python
result = await client.send_message(
    chat_id=123456789,
    text="Привет!",
    parse_mode="HTML"
)
```

#### `answer_callback_query(callback_query_id, text=None)`
Ответ на callback запрос.

```python
result = await client.answer_callback_query(
    callback_query_id="callback_id",
    text="Обработано"
)
```

## Constructor

Система создания ботов без программирования.

### EnhancedConstructorBot

Расширенный конструктор с полной настройкой.

```python
from constructor.dialog.enhanced_constructor import EnhancedConstructorBot

constructor = EnhancedConstructorBot("YOUR_TOKEN")
constructor.run()
```

### Команды конструктора

- `/start` - Начать работу
- `/create` - Создать нового бота
- `/customize` - Настроить существующий бот
- `/preview` - Предпросмотр бота
- `/help` - Справка
- `/cancel` - Отменить создание
- `/status` - Статус создания

### Процесс создания

1. Выбор типа бота (5 шаблонов)
2. Ввод имени и описания
3. Настройка команд и ответов
4. Предпросмотр
5. Генерация кода

### Шаблоны ботов

1. **Простой бот** - базовые команды
2. **Эхо-бот** - повторение сообщений
3. **FAQ бот** - часто задаваемые вопросы
4. **Магазин бот** - интернет-магазин
5. **Кастомный бот** - настраиваемый

### Пример использования

```python
# Создание бота-конструктора
from constructor.dialog.enhanced_constructor import EnhancedConstructorBot

constructor = EnhancedConstructorBot("YOUR_TOKEN")

# Запуск
constructor.run()
```

## Примеры использования

Смотрите папку `examples/` для полных примеров:

- `simple_bot.py` - Простой бот
- `echo_bot.py` - Эхо-бот
- `faq_bot.py` - FAQ бот
- `shop_bot.py` - Магазин-бот
- `constructor_bot.py` - Базовый конструктор
- `enhanced_constructor_bot.py` - Расширенный конструктор
