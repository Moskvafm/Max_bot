"""
Базовые классы для middleware
"""

from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable
from ..core.types import Update


class BaseMiddleware(ABC):
    """Базовый класс для middleware"""
    
    @abstractmethod
    async def __call__(
        self,
        handler: Callable[[Update], Awaitable[Any]],
        update: Update
    ) -> Any:
        """Вызов middleware"""
        pass


class LoggingMiddleware(BaseMiddleware):
    """Middleware для логирования"""
    
    def __init__(self, logger=None):
        self.logger = logger
    
    async def __call__(
        self,
        handler: Callable[[Update], Awaitable[Any]],
        update: Update
    ) -> Any:
        if self.logger:
            self.logger.info(f"Processing update {update.update_id}")
        
        try:
            result = await handler(update)
            if self.logger:
                self.logger.info(f"Update {update.update_id} processed successfully")
            return result
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error processing update {update.update_id}: {e}")
            raise


class ThrottlingMiddleware(BaseMiddleware):
    """Middleware для ограничения частоты запросов"""
    
    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit
        self.last_request = {}
    
    async def __call__(
        self,
        handler: Callable[[Update], Awaitable[Any]],
        update: Update
    ) -> Any:
        import asyncio
        import time
        
        # Определяем пользователя
        user_id = None
        if update.message and update.message.from_user:
            user_id = update.message.from_user.id
        elif update.callback_query and update.callback_query.from_user:
            user_id = update.callback_query.from_user.id
        
        if user_id:
            current_time = time.time()
            if user_id in self.last_request:
                time_diff = current_time - self.last_request[user_id]
                if time_diff < self.rate_limit:
                    await asyncio.sleep(self.rate_limit - time_diff)
            
            self.last_request[user_id] = time.time()
        
        return await handler(update)


class ErrorHandlingMiddleware(BaseMiddleware):
    """Middleware для обработки ошибок"""
    
    def __init__(self, error_handler: Callable[[Exception, Update], Awaitable[Any]] = None):
        self.error_handler = error_handler
    
    async def __call__(
        self,
        handler: Callable[[Update], Awaitable[Any]],
        update: Update
    ) -> Any:
        try:
            return await handler(update)
        except Exception as e:
            if self.error_handler:
                return await self.error_handler(e, update)
            raise
