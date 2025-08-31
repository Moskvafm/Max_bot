"""
Базовые классы для обработчиков
"""

import asyncio
from typing import Callable, Any, Awaitable, Union, List
from .types import Update, Message, CallbackQuery
from ..filters.base import BaseFilter


class Handler:
    """Базовый класс для обработчиков"""
    
    def __init__(
        self,
        callback: Callable[[Update], Awaitable[Any]],
        filters: Union[BaseFilter, List[BaseFilter]] = None
    ):
        self.callback = callback
        self.filters = filters if isinstance(filters, list) else [filters] if filters else []
    
    async def check(self, update: Update) -> bool:
        """Проверка фильтров"""
        if not self.filters:
            return True
        
        for filter_obj in self.filters:
            if not await filter_obj.check(update):
                return False
        return True
    
    async def handle(self, update: Update) -> Any:
        """Обработка обновления"""
        if await self.check(update):
            return await self.callback(update)
        return None


class MessageHandler(Handler):
    """Обработчик сообщений"""
    
    def __init__(
        self,
        callback: Callable[[Message], Awaitable[Any]],
        filters: Union[BaseFilter, List[BaseFilter]] = None
    ):
        super().__init__(callback, filters)
    
    async def handle(self, update: Update) -> Any:
        """Обработка сообщения"""
        if update.message and await self.check(update):
            return await self.callback(update.message)
        return None


class CallbackQueryHandler(Handler):
    """Обработчик callback запросов"""
    
    def __init__(
        self,
        callback: Callable[[CallbackQuery], Awaitable[Any]],
        filters: Union[BaseFilter, List[BaseFilter]] = None
    ):
        super().__init__(callback, filters)
    
    async def handle(self, update: Update) -> Any:
        """Обработка callback запроса"""
        if update.callback_query and await self.check(update):
            return await self.callback(update.callback_query)
        return None


def message_handler(filters: Union[BaseFilter, List[BaseFilter]] = None):
    """Декоратор для обработчиков сообщений"""
    def decorator(func: Callable[[Message], Awaitable[Any]]) -> MessageHandler:
        return MessageHandler(func, filters)
    return decorator


def callback_query_handler(filters: Union[BaseFilter, List[BaseFilter]] = None):
    """Декоратор для обработчиков callback запросов"""
    def decorator(func: Callable[[CallbackQuery], Awaitable[Any]]) -> CallbackQueryHandler:
        return CallbackQueryHandler(func, filters)
    return decorator
