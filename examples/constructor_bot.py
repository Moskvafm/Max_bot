"""
Пример запуска бота-конструктора
"""

import os
from constructor.dialog.constructor_bot import ConstructorBot


def main():
    """Запуск бота-конструктора"""
    # Токен и база API из окружения
    token = os.getenv("MAX_BOT_TOKEN", "YOUR_CONSTRUCTOR_BOT_TOKEN")
    base_url = os.getenv("MAX_API_BASE_URL")
    
    # Создаем и запускаем бота-конструктор
    constructor = ConstructorBot(token, base_url=base_url)
    
    print("🤖 MAX Bot Constructor запущен!")
    print("Используйте команды:")
    print("/start - Начать работу")
    print("/help - Справка")
    print("/create - Создать нового бота")
    
    try:
        constructor.run()
    except KeyboardInterrupt:
        print("\n👋 Бот-конструктор остановлен")


if __name__ == "__main__":
    main()
