"""
Базовые типы данных для MAX Bot Library
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class User:
    """Пользователь MAX"""
    id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_bot: bool = False


@dataclass
class Chat:
    """Чат в MAX"""
    id: int
    type: str  # 'private', 'group', 'supergroup', 'channel'
    title: Optional[str] = None
    username: Optional[str] = None


@dataclass
class Message:
    """Сообщение в MAX"""
    message_id: int
    date: datetime
    chat: Chat
    from_user: Optional[User] = None
    text: Optional[str] = None
    caption: Optional[str] = None
    reply_to_message: Optional['Message'] = None
    entities: List[Dict[str, Any]] = None


@dataclass
class CallbackQuery:
    """Callback запрос"""
    id: str
    from_user: User
    message: Optional[Message] = None
    data: Optional[str] = None


@dataclass
class Update:
    """Обновление от MAX API"""
    update_id: int
    message: Optional[Message] = None
    callback_query: Optional[CallbackQuery] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None


@dataclass
class BotCommand:
    """Команда бота"""
    command: str
    description: str


@dataclass
class BotInfo:
    """Информация о боте"""
    id: int
    username: str
    first_name: str
    can_join_groups: bool = False
    can_read_all_group_messages: bool = False
    supports_inline_queries: bool = False
