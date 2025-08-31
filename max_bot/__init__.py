"""
MAX Bot Library - аналог aiogram для платформы MAX

Основная библиотека для создания ботов в приложении MAX
с поддержкой асинхронных методов и модульной архитектуры.
"""

from .core.dispatcher import Dispatcher
from .core.router import Router
from .core.handler import Handler
from .core.types import Update, Message, CallbackQuery
from .filters.base import BaseFilter
from .middleware.base import BaseMiddleware

__version__ = "0.1.0"
__author__ = "maksimmerlin"

__all__ = [
    "Dispatcher",
    "Router", 
    "Handler",
    "Update",
    "Message",
    "CallbackQuery",
    "BaseFilter",
    "BaseMiddleware"
]
