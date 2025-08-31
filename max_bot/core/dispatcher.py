"""
Основной диспетчер для MAX Bot Library
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any
from .router import Router
from .types import Update, BotInfo
from ..middleware.base import BaseMiddleware


class Dispatcher:
    """Основной диспетчер для управления ботом"""
    
    def __init__(self, token: str = None):
        self.token = token
        self.router = Router("main")
        self.middlewares: List[BaseMiddleware] = []
        self.logger = logging.getLogger(__name__)
        self._running = False
        
        # Настройка логирования
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def include_router(self, router: Router):
        """Включение роутера"""
        self.router.include_router(router)
    
    def add_middleware(self, middleware: BaseMiddleware):
        """Добавление middleware"""
        self.middlewares.append(middleware)
    
    async def process_update(self, update: Update) -> Any:
        """Обработка обновления"""
        self.logger.debug(f"Processing update {update.update_id}")
        
        # Применяем middleware
        handler = self.router.handle
        for middleware in reversed(self.middlewares):
            handler = lambda h=handler, m=middleware: m(h, update)
        
        try:
            result = await handler(update)
            self.logger.debug(f"Update {update.update_id} processed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Error processing update {update.update_id}: {e}")
            raise
    
    async def start_polling(self, timeout: int = 30, limit: int = 100):
        """Запуск polling для получения обновлений"""
        if not self.token:
            raise ValueError("Token is required for polling")
        
        self._running = True
        self.logger.info("Starting polling...")
        
        try:
            while self._running:
                try:
                    # Здесь будет логика получения обновлений от MAX API
                    # Пока заглушка
                    await asyncio.sleep(1)
                except Exception as e:
                    self.logger.error(f"Polling error: {e}")
                    await asyncio.sleep(5)
        except KeyboardInterrupt:
            self.logger.info("Polling stopped by user")
        finally:
            self._running = False
    
    def stop_polling(self):
        """Остановка polling"""
        self._running = False
        self.logger.info("Polling stopped")
    
    async def get_me(self) -> Optional[BotInfo]:
        """Получение информации о боте"""
        if not self.token:
            return None
        
        # Здесь будет запрос к MAX API
        # Пока заглушка
        return BotInfo(
            id=123456789,
            username="test_bot",
            first_name="Test Bot"
        )
    
    def message_handler(self, filters=None):
        """Декоратор для регистрации обработчика сообщений"""
        return self.router.message_handler(filters)
    
    def callback_query_handler(self, filters=None):
        """Декоратор для регистрации обработчика callback запросов"""
        return self.router.callback_query_handler(filters)
    
    def run(self, token: str = None):
        """Запуск бота"""
        if token:
            self.token = token
        
        if not self.token:
            raise ValueError("Token is required")
        
        try:
            asyncio.run(self.start_polling())
        except KeyboardInterrupt:
            self.logger.info("Bot stopped")
