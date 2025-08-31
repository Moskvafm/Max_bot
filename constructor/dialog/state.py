"""
Система состояний для диалогового конструктора
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List


class BotType(Enum):
    """Типы ботов"""
    SIMPLE = "simple"
    ECHO = "echo"
    FAQ = "faq"
    SHOP = "shop"
    CUSTOM = "custom"


class DialogState(Enum):
    """Состояния диалога"""
    START = "start"
    CHOOSE_TYPE = "choose_type"
    BOT_NAME = "bot_name"
    BOT_DESCRIPTION = "bot_description"
    COMMANDS = "commands"
    RESPONSES = "responses"
    CUSTOMIZE_COMMANDS = "customize_commands"
    CUSTOMIZE_RESPONSES = "customize_responses"
    SETTINGS = "settings"
    CONFIRM = "confirm"
    FINISHED = "finished"


@dataclass
class BotConfig:
    """Конфигурация бота"""
    name: str = ""
    description: str = ""
    bot_type: BotType = BotType.SIMPLE
    commands: List[Dict[str, str]] = field(default_factory=list)
    responses: Dict[str, str] = field(default_factory=dict)
    settings: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            "name": self.name,
            "description": self.description,
            "bot_type": self.bot_type.value,
            "commands": self.commands,
            "responses": self.responses,
            "settings": self.settings
        }


@dataclass
class DialogSession:
    """Сессия диалога"""
    user_id: int
    state: DialogState = DialogState.START
    config: BotConfig = field(default_factory=BotConfig)
    temp_data: Dict[str, Any] = field(default_factory=dict)
    
    def reset(self):
        """Сброс сессии"""
        self.state = DialogState.START
        self.config = BotConfig()
        self.temp_data = {}


class DialogManager:
    """Менеджер диалогов"""
    
    def __init__(self):
        self.sessions: Dict[int, DialogSession] = {}
    
    def get_session(self, user_id: int) -> DialogSession:
        """Получение или создание сессии"""
        if user_id not in self.sessions:
            self.sessions[user_id] = DialogSession(user_id)
        return self.sessions[user_id]
    
    def set_state(self, user_id: int, state: DialogState):
        """Установка состояния"""
        session = self.get_session(user_id)
        session.state = state
    
    def get_state(self, user_id: int) -> DialogState:
        """Получение состояния"""
        session = self.get_session(user_id)
        return session.state
    
    def update_config(self, user_id: int, **kwargs):
        """Обновление конфигурации"""
        session = self.get_session(user_id)
        for key, value in kwargs.items():
            if hasattr(session.config, key):
                setattr(session.config, key, value)
    
    def get_config(self, user_id: int) -> BotConfig:
        """Получение конфигурации"""
        session = self.get_session(user_id)
        return session.config
    
    def reset_session(self, user_id: int):
        """Сброс сессии"""
        if user_id in self.sessions:
            self.sessions[user_id].reset()
    
    def remove_session(self, user_id: int):
        """Удаление сессии"""
        if user_id in self.sessions:
            del self.sessions[user_id]
