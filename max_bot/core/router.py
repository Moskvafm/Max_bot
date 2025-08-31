"""
Роутер для организации обработчиков
"""

from typing import List, Optional
from .handler import Handler, MessageHandler, CallbackQueryHandler
from ..filters.base import BaseFilter


class Router:
    """Роутер для организации обработчиков"""
    
    def __init__(self, name: str = None):
        self.name = name or f"router_{id(self)}"
        self.handlers: List[Handler] = []
        self.middlewares: List = []
    
    def message_handler(self, filters: BaseFilter = None):
        """Декоратор для регистрации обработчика сообщений"""
        def decorator(func):
            handler = MessageHandler(func, filters)
            self.handlers.append(handler)
            return func
        return decorator
    
    def callback_query_handler(self, filters: BaseFilter = None):
        """Декоратор для регистрации обработчика callback запросов"""
        def decorator(func):
            handler = CallbackQueryHandler(func, filters)
            self.handlers.append(handler)
            return func
        return decorator
    
    def include_router(self, router: 'Router'):
        """Включение другого роутера"""
        self.handlers.extend(router.handlers)
        self.middlewares.extend(router.middlewares)
    
    def add_handler(self, handler: Handler):
        """Добавление обработчика"""
        self.handlers.append(handler)
    
    def add_middleware(self, middleware):
        """Добавление middleware"""
        self.middlewares.append(middleware)
    
    async def handle(self, update):
        """Обработка обновления через все обработчики"""
        for handler in self.handlers:
            result = await handler.handle(update)
            if result is not None:
                return result
        return None
    
    def __len__(self):
        return len(self.handlers)
    
    def __iter__(self):
        return iter(self.handlers)
