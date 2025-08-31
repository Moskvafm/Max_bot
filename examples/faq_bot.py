"""
Пример FAQ бота с использованием MAX Bot Library
"""

from max_bot import Dispatcher
from max_bot.filters.base import command, text
from max_bot.middleware.base import LoggingMiddleware


# Создаем диспетчер
dp = Dispatcher("YOUR_BOT_TOKEN")

# База знаний FAQ
faq_database = {
    "как работает бот": "Этот бот отвечает на часто задаваемые вопросы. Просто задайте вопрос!",
    "где получить помощь": "Для получения помощи обратитесь к администратору или используйте команду /help",
    "контакты поддержки": "Email: support@example.com\nТелефон: +7 (999) 123-45-67",
    "часы работы": "Мы работаем с 9:00 до 18:00 по московскому времени",
    "цены": "Актуальные цены можно узнать на нашем сайте или у менеджера",
    "доставка": "Доставка осуществляется по всей России. Сроки: 1-3 дня",
    "возврат": "Возврат товара возможен в течение 14 дней с момента покупки"
}


@dp.message_handler(command("start"))
async def start_command(message):
    """Обработчик команды /start"""
    await message.answer("Привет! Я FAQ бот. Задавайте мне вопросы, и я постараюсь на них ответить!")


@dp.message_handler(command("help"))
async def help_command(message):
    """Обработчик команды /help"""
    help_text = """
FAQ бот - отвечает на часто задаваемые вопросы

Команды:
/start - Начать работу с ботом
/help - Показать эту справку
/faq - Список популярных вопросов
/ask - Задать вопрос

Просто напишите ваш вопрос, и я постараюсь на него ответить!
    """
    await message.answer(help_text)


@dp.message_handler(command("faq"))
async def faq_command(message):
    """Обработчик команды /faq"""
    faq_text = "Часто задаваемые вопросы:\n\n"
    for i, question in enumerate(faq_database.keys(), 1):
        faq_text += f"{i}. {question}\n"
    faq_text += "\nЗадайте любой из этих вопросов или свой собственный!"
    await message.answer(faq_text)


@dp.message_handler(command("ask"))
async def ask_command(message):
    """Обработчик команды /ask"""
    await message.answer("Введите ваш вопрос:")


@dp.message_handler()
async def question_handler(message):
    """Обработчик вопросов"""
    question = message.text.lower().strip()
    
    # Ищем ответ в базе знаний
    for key, answer in faq_database.items():
        if key in question or question in key:
            await message.answer(answer)
            return
    
    # Если ответ не найден
    await message.answer("Извините, я не знаю ответ на этот вопрос. Обратитесь к администратору или попробуйте переформулировать вопрос.")


if __name__ == "__main__":
    # Добавляем middleware
    dp.add_middleware(LoggingMiddleware())
    
    # Запускаем бота
    dp.run()
