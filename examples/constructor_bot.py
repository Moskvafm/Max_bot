"""
Пример запуска бота-конструктора
"""

from constructor.dialog.constructor_bot import ConstructorBot


def main():
    """Запуск бота-конструктора"""
    # Замените на ваш токен
    token = "YOUR_CONSTRUCTOR_BOT_TOKEN"
    
    # Создаем и запускаем бота-конструктор
    constructor = ConstructorBot(token)
    
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
