"""
Пример эхо-бота с использованием MAX Bot Library
"""

from max_bot import Dispatcher
from max_bot.filters.base import command, text
from max_bot.middleware.base import LoggingMiddleware, ThrottlingMiddleware


# Создаем диспетчер
dp = Dispatcher("YOUR_BOT_TOKEN")


@dp.message_handler(command("start"))
async def start_command(message):
    """Обработчик команды /start"""
    await message.answer("Привет! Я эхо-бот. Отправляйте мне сообщения, и я их повторю!")


@dp.message_handler(command("help"))
async def help_command(message):
    """Обработчик команды /help"""
    help_text = """
Эхо-бот - повторяет ваши сообщения

Команды:
/start - Начать работу с ботом
/help - Показать эту справку
/stop - Остановить эхо

Просто отправьте любое сообщение, и я его повторю!
    """
    await message.answer(help_text)


@dp.message_handler(command("stop"))
async def stop_command(message):
    """Обработчик команды /stop"""
    await message.answer("Эхо остановлено. Используйте /start для возобновления.")


@dp.message_handler(text("привет"))
async def hello_handler(message):
    """Обработчик текста 'привет'"""
    await message.answer("Привет! Отправляйте мне сообщения, и я их повторю!")


@dp.message_handler()
async def echo_handler(message):
    """Эхо-обработчик для всех остальных сообщений"""
    echo_text = f"Эхо: {message.text}"
    await message.answer(echo_text)


if __name__ == "__main__":
    # Добавляем middleware
    dp.add_middleware(LoggingMiddleware())
    dp.add_middleware(ThrottlingMiddleware(rate_limit=1.0))
    
    # Запускаем бота
    dp.run()
