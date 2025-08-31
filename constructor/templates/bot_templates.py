"""
Шаблоны ботов для конструктора
"""

from typing import Dict, List, Any
from ..dialog.state import BotType, BotConfig


class BotTemplates:
    """Шаблоны ботов"""
    
    @staticmethod
    def get_template(bot_type: BotType) -> Dict[str, Any]:
        """Получение шаблона по типу"""
        templates = {
            BotType.SIMPLE: BotTemplates._simple_bot(),
            BotType.ECHO: BotTemplates._echo_bot(),
            BotType.FAQ: BotTemplates._faq_bot(),
            BotType.SHOP: BotTemplates._shop_bot(),
            BotType.CUSTOM: BotTemplates._custom_bot()
        }
        return templates.get(bot_type, BotTemplates._simple_bot())
    
    @staticmethod
    def _simple_bot() -> Dict[str, Any]:
        """Простой бот"""
        return {
            "name": "Простой бот",
            "description": "Базовый бот с основными командами",
            "commands": [
                {"command": "start", "description": "Начать работу с ботом"},
                {"command": "help", "description": "Показать справку"},
                {"command": "info", "description": "Информация о боте"}
            ],
            "responses": {
                "start": "Привет! Я простой бот. Чем могу помочь?",
                "help": "Доступные команды:\n/start - Начать работу\n/help - Справка\n/info - Информация",
                "info": "Я простой бот, созданный с помощью конструктора.",
                "default": "Не понимаю эту команду. Используйте /help для справки."
            },
            "settings": {
                "auto_reply": True,
                "welcome_message": True
            }
        }
    
    @staticmethod
    def _echo_bot() -> Dict[str, Any]:
        """Эхо-бот"""
        return {
            "name": "Эхо-бот",
            "description": "Бот, который повторяет ваши сообщения",
            "commands": [
                {"command": "start", "description": "Начать работу с ботом"},
                {"command": "help", "description": "Показать справку"},
                {"command": "stop", "description": "Остановить эхо"}
            ],
            "responses": {
                "start": "Привет! Я эхо-бот. Отправляйте мне сообщения, и я их повторю!",
                "help": "Просто отправьте мне любое сообщение, и я его повторю.\n/stop - остановить эхо",
                "stop": "Эхо остановлено. Используйте /start для возобновления.",
                "echo": "Вы сказали: {message}",
                "default": "Эхо: {message}"
            },
            "settings": {
                "echo_enabled": True,
                "prefix": "Эхо: "
            }
        }
    
    @staticmethod
    def _faq_bot() -> Dict[str, Any]:
        """FAQ бот"""
        return {
            "name": "FAQ бот",
            "description": "Бот для ответов на часто задаваемые вопросы",
            "commands": [
                {"command": "start", "description": "Начать работу с ботом"},
                {"command": "help", "description": "Показать справку"},
                {"command": "faq", "description": "Список вопросов"},
                {"command": "ask", "description": "Задать вопрос"}
            ],
            "responses": {
                "start": "Привет! Я FAQ бот. Задавайте мне вопросы!",
                "help": "Команды:\n/faq - список вопросов\n/ask - задать вопрос",
                "faq": "Часто задаваемые вопросы:\n1. Как работает бот?\n2. Где получить помощь?\n3. Контакты поддержки",
                "ask": "Введите ваш вопрос:",
                "default": "Извините, я не знаю ответ на этот вопрос. Обратитесь к администратору."
            },
            "settings": {
                "faq_enabled": True,
                "auto_suggest": True
            }
        }
    
    @staticmethod
    def _shop_bot() -> Dict[str, Any]:
        """Магазин бот"""
        return {
            "name": "Магазин бот",
            "description": "Бот для интернет-магазина",
            "commands": [
                {"command": "start", "description": "Начать работу с ботом"},
                {"command": "help", "description": "Показать справку"},
                {"command": "catalog", "description": "Каталог товаров"},
                {"command": "cart", "description": "Корзина"},
                {"command": "order", "description": "Оформить заказ"}
            ],
            "responses": {
                "start": "Добро пожаловать в наш магазин! Чем могу помочь?",
                "help": "Команды:\n/catalog - каталог товаров\n/cart - корзина\n/order - оформить заказ",
                "catalog": "Каталог товаров:\n1. Товар 1 - 100₽\n2. Товар 2 - 200₽\n3. Товар 3 - 300₽",
                "cart": "Ваша корзина пуста. Добавьте товары из каталога!",
                "order": "Для оформления заказа свяжитесь с менеджером.",
                "default": "Выберите команду из меню или используйте /help для справки."
            },
            "settings": {
                "shop_enabled": True,
                "payment_enabled": False
            }
        }
    
    @staticmethod
    def _custom_bot() -> Dict[str, Any]:
        """Кастомный бот"""
        return {
            "name": "Кастомный бот",
            "description": "Настраиваемый бот под ваши нужды",
            "commands": [],
            "responses": {},
            "settings": {
                "custom_enabled": True,
                "flexible": True
            }
        }
    
    @staticmethod
    def get_all_templates() -> Dict[str, Dict[str, Any]]:
        """Получение всех шаблонов"""
        return {
            "simple": BotTemplates._simple_bot(),
            "echo": BotTemplates._echo_bot(),
            "faq": BotTemplates._faq_bot(),
            "shop": BotTemplates._shop_bot(),
            "custom": BotTemplates._custom_bot()
        }
    
    @staticmethod
    def apply_template(config: BotConfig, template: Dict[str, Any]):
        """Применение шаблона к конфигурации"""
        config.name = template.get("name", config.name)
        config.description = template.get("description", config.description)
        config.commands = template.get("commands", config.commands)
        config.responses = template.get("responses", config.responses)
        config.settings.update(template.get("settings", {}))
