"""
Пример расширенного бота-конструктора
"""

from constructor.dialog.enhanced_constructor import EnhancedConstructorBot


def main():
    """Запуск расширенного бота-конструктора"""
    # Замените на ваш токен
    token = "YOUR_ENHANCED_CONSTRUCTOR_BOT_TOKEN"
    
    # Создаем и запускаем расширенный бот-конструктор
    constructor = EnhancedConstructorBot(token)
    
    print("🤖 MAX Bot Constructor Pro запущен!")
    print("Расширенные возможности:")
    print("✅ Полная настройка команд")
    print("✅ Редактирование ответов")
    print("✅ Предпросмотр бота")
    print("✅ Валидация данных")
    print("✅ Генерация кода")
    print()
    print("Используйте команды:")
    print("/start - Начать работу")
    print("/create - Создать нового бота")
    print("/customize - Настроить существующий бот")
    print("/preview - Предпросмотр бота")
    print("/help - Справка")
    
    try:
        constructor.run()
    except KeyboardInterrupt:
        print("\n👋 Расширенный бот-конструктор остановлен")


if __name__ == "__main__":
    main()
