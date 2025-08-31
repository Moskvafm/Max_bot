"""
HTTP клиент для MAX API
"""

import aiohttp
import json
from typing import Dict, Any, Optional
from ..core.types import Update, BotInfo


class MaxAPIClient:
    """Клиент для работы с MAX API"""
    
    def __init__(self, token: str, base_url: str = "https://api.max.ru"):
        self.token = token
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _request(self, method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """Выполнение HTTP запроса"""
        if not self.session:
            raise RuntimeError("Session not initialized. Use async context manager.")
        
        url = f"{self.base_url}/bot{self.token}/{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        async with self.session.request(method, url, json=data, headers=headers) as response:
            return await response.json()
    
    async def get_me(self) -> BotInfo:
        """Получение информации о боте"""
        data = await self._request("GET", "getMe")
        return BotInfo(**data["result"])
    
    async def get_updates(self, offset: int = None, limit: int = 100) -> list[Update]:
        """Получение обновлений"""
        params = {}
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        
        data = await self._request("GET", "getUpdates", params)
        return [Update(**update) for update in data["result"]]
    
    async def send_message(self, chat_id: int, text: str, **kwargs) -> Dict[str, Any]:
        """Отправка сообщения"""
        data = {"chat_id": chat_id, "text": text, **kwargs}
        return await self._request("POST", "sendMessage", data)
    
    async def answer_callback_query(self, callback_query_id: str, text: str = None) -> Dict[str, Any]:
        """Ответ на callback запрос"""
        data = {"callback_query_id": callback_query_id}
        if text:
            data["text"] = text
        return await self._request("POST", "answerCallbackQuery", data)
