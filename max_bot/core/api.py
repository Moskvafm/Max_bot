"""
HTTP клиент для интеграции с Bot API мессенджера MAX.

Заметка: названия эндпоинтов и структура JSON могут отличаться в реальной
документации MAX. Эти методы написаны так, чтобы их было легко адаптировать
под фактический Bot API: базовый URL, пути, параметры и парсинг можно
сконфигурировать через параметры конструктора.
"""

from __future__ import annotations

import asyncio
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import httpx

from .types import Update, Message, Chat, User


def _ts_to_datetime(ts: int) -> datetime:
    try:
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    except Exception:
        # На случай, если timestamp в миллисекундах
        return datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc)


class MaxApiClient:
    """Асинхронный HTTP-клиент для MAX Bot API."""

    def __init__(
        self,
        token: str,
        base_url: str = "https://api.max.example.com/bot",
        get_updates_path: str = "/getUpdates",
        send_message_path: str = "/sendMessage",
        timeout: float = 30.0,
    ) -> None:
        if not token:
            raise ValueError("Token is required for MaxApiClient")
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.get_updates_path = get_updates_path
        self.send_message_path = send_message_path
        self.client = httpx.AsyncClient(timeout=timeout)

    async def close(self) -> None:
        await self.client.aclose()

    def _url(self, path: str) -> str:
        return f"{self.base_url}{self.token}{path}"

    async def get_updates(
        self, offset: Optional[int] = None, timeout: int = 30, limit: int = 100
    ) -> List[Update]:
        params: Dict[str, Any] = {"timeout": timeout, "limit": limit}
        if offset is not None:
            params["offset"] = offset
        resp = await self.client.get(self._url(self.get_updates_path), params=params)
        resp.raise_for_status()
        data = resp.json()

        # Ожидаем telegram-подобную форму {ok: bool, result: [...]}
        result = data.get("result", data)
        updates: List[Update] = []
        for item in result:
            update = self._parse_update(item)
            if update:
                updates.append(update)
        return updates

    async def send_message(self, chat_id: int, text: str) -> Message:
        payload = {"chat_id": chat_id, "text": text}
        resp = await self.client.post(self._url(self.send_message_path), json=payload)
        resp.raise_for_status()
        data = resp.json()
        message_obj = data.get("result", data)
        return self._parse_message(message_obj)

    def _parse_user(self, raw: Dict[str, Any]) -> User:
        return User(
            id=raw.get("id") or raw.get("user_id"),
            username=raw.get("username"),
            first_name=raw.get("first_name"),
            last_name=raw.get("last_name"),
            is_bot=bool(raw.get("is_bot", False)),
        )

    def _parse_chat(self, raw: Dict[str, Any]) -> Chat:
        return Chat(
            id=raw.get("id") or raw.get("chat_id"),
            type=raw.get("type", "private"),
            title=raw.get("title"),
            username=raw.get("username"),
        )

    def _parse_message(self, raw: Dict[str, Any]) -> Message:
        from_user_raw = raw.get("from") or raw.get("from_user")
        chat_raw = raw.get("chat") or {"id": raw.get("peer_id")}
        date_raw = raw.get("date") or raw.get("timestamp")
        text = raw.get("text") or raw.get("body") or raw.get("caption")

        msg = Message(
            message_id=raw.get("message_id") or raw.get("id"),
            date=_ts_to_datetime(date_raw) if date_raw else datetime.now(timezone.utc),
            chat=self._parse_chat(chat_raw) if chat_raw else Chat(id=0, type="private"),
            from_user=self._parse_user(from_user_raw) if from_user_raw else None,
            text=text,
            caption=raw.get("caption"),
            reply_to_message=None,
            entities=raw.get("entities"),
        )
        # Инъекция клиента для методов-ответов
        setattr(msg, "_api_client", self)
        return msg

    def _parse_update(self, raw: Dict[str, Any]) -> Optional[Update]:
        update_id = raw.get("update_id") or raw.get("id")
        message_raw = raw.get("message") or raw.get("message_new") or raw.get("event_message")
        callback_raw = raw.get("callback_query")

        message = self._parse_message(message_raw) if message_raw else None
        # callback парсинг опущен до появления спецификации
        return Update(update_id=update_id, message=message)

