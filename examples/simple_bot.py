"""
Пример простого бота с использованием MAX Bot Library
"""

import os
import asyncio
from max_bot import Dispatcher
from max_bot.filters.base import command, text


# Читаем конфиг из окружения
TOKEN = os.getenv("MAX_BOT_TOKEN", "YOUR_BOT_TOKEN")
BASE_URL = os.getenv("MAX_API_BASE_URL")  # например, https://api.max.example.com/bot

# Создаем диспетчер
dp = Dispatcher(TOKEN, base_url=BASE_URL)


@dp.message_handler(command("start"))
async def start_command(message):
    """Обработчик команды /start"""
    await message.answer("Привет! Я бот, созданный с помощью MAX Bot Library!")


@dp.message_handler(command("help"))
async def help_command(message):
    """Обработчик команды /help"""
    help_text = """
Доступные команды:
/start - Начать работу с ботом
/help - Показать эту справку
/info - Информация о боте
    """
    await message.answer(help_text)


@dp.message_handler(command("info"))
async def info_command(message):
    """Обработчик команды /info"""
    bot_info = await dp.get_me()
    info_text = f"""
Информация о боте:
ID: {bot_info.id}
Username: @{bot_info.username}
Имя: {bot_info.first_name}
    """
    await message.answer(info_text)


@dp.message_handler(text("привет"))
async def hello_handler(message):
    """Обработчик текста 'привет'"""
    await message.answer("Привет! Как дела?")


@dp.message_handler()
async def echo_handler(message):
    """Эхо-обработчик для всех остальных сообщений"""
    await message.answer(f"Вы сказали: {message.text}")


if __name__ == "__main__":
    # Запускаем бота
    dp.run()
