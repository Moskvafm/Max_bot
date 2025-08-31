"""
Базовые фильтры для MAX Bot Library
"""

from abc import ABC, abstractmethod
from typing import Union, List
from ..core.types import Update, Message, CallbackQuery


class BaseFilter(ABC):
    """Базовый класс для фильтров"""
    
    @abstractmethod
    async def check(self, update: Update) -> bool:
        """Проверка фильтра"""
        pass


class TextFilter(BaseFilter):
    """Фильтр по тексту сообщения"""
    
    def __init__(self, text: Union[str, List[str]]):
        self.texts = [text] if isinstance(text, str) else text
    
    async def check(self, update: Update) -> bool:
        if not update.message or not update.message.text:
            return False
        return update.message.text in self.texts


class CommandFilter(BaseFilter):
    """Фильтр по командам"""
    
    def __init__(self, command: Union[str, List[str]]):
        self.commands = [command] if isinstance(command, str) else command
    
    async def check(self, update: Update) -> bool:
        if not update.message or not update.message.text:
            return False
        
        text = update.message.text.strip()
        if not text.startswith('/'):
            return False
        
        command = text.split()[0][1:]  # Убираем '/'
        return command in self.commands


class CallbackDataFilter(BaseFilter):
    """Фильтр по данным callback"""
    
    def __init__(self, data: Union[str, List[str]]):
        self.data_list = [data] if isinstance(data, str) else data
    
    async def check(self, update: Update) -> bool:
        if not update.callback_query or not update.callback_query.data:
            return False
        return update.callback_query.data in self.data_list


class ChatTypeFilter(BaseFilter):
    """Фильтр по типу чата"""
    
    def __init__(self, chat_type: Union[str, List[str]]):
        self.chat_types = [chat_type] if isinstance(chat_type, str) else chat_type
    
    async def check(self, update: Update) -> bool:
        if not update.message or not update.message.chat:
            return False
        return update.message.chat.type in self.chat_types


class UserFilter(BaseFilter):
    """Фильтр по пользователю"""
    
    def __init__(self, user_id: Union[int, List[int]]):
        self.user_ids = [user_id] if isinstance(user_id, int) else user_id
    
    async def check(self, update: Update) -> bool:
        if update.message and update.message.from_user:
            return update.message.from_user.id in self.user_ids
        if update.callback_query and update.callback_query.from_user:
            return update.callback_query.from_user.id in self.user_ids
        return False


# Удобные функции для создания фильтров
def text(text: Union[str, List[str]]) -> TextFilter:
    return TextFilter(text)


def command(command: Union[str, List[str]]) -> CommandFilter:
    return CommandFilter(command)


def callback_data(data: Union[str, List[str]]) -> CallbackDataFilter:
    return CallbackDataFilter(data)


def chat_type(chat_type: Union[str, List[str]]) -> ChatTypeFilter:
    return ChatTypeFilter(chat_type)


def user(user_id: Union[int, List[int]]) -> UserFilter:
    return UserFilter(user_id)
