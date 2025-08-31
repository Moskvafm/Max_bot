"""
Базовые тесты для MAX Bot Library
"""

import pytest
import asyncio
from datetime import datetime
from max_bot.core.types import User, Chat, Message, Update, BotInfo
from max_bot.core.router import Router
from max_bot.core.handler import MessageHandler
from max_bot.filters.base import TextFilter, CommandFilter
from max_bot.dialog.state import BotConfig, BotType, DialogManager, DialogState


class TestTypes:
    """Тесты для типов данных"""
    
    def test_user_creation(self):
        """Тест создания пользователя"""
        user = User(id=123, username="test_user", first_name="Test")
        assert user.id == 123
        assert user.username == "test_user"
        assert user.first_name == "Test"
        assert not user.is_bot
    
    def test_chat_creation(self):
        """Тест создания чата"""
        chat = Chat(id=456, type="private", title="Test Chat")
        assert chat.id == 456
        assert chat.type == "private"
        assert chat.title == "Test Chat"
    
    def test_message_creation(self):
        """Тест создания сообщения"""
        user = User(id=123, username="test_user")
        chat = Chat(id=456, type="private")
        message = Message(
            message_id=1,
            date=datetime.now(),
            chat=chat,
            from_user=user,
            text="Hello, world!"
        )
        assert message.message_id == 1
        assert message.text == "Hello, world!"
        assert message.from_user.id == 123


class TestFilters:
    """Тесты для фильтров"""
    
    @pytest.mark.asyncio
    async def test_text_filter(self):
        """Тест фильтра по тексту"""
        filter_obj = TextFilter("hello")
        user = User(id=123)
        chat = Chat(id=456, type="private")
        message = Message(
            message_id=1,
            date=datetime.now(),
            chat=chat,
            from_user=user,
            text="hello"
        )
        update = Update(update_id=1, message=message)
        
        result = await filter_obj.check(update)
        assert result is True
    
    @pytest.mark.asyncio
    async def test_command_filter(self):
        """Тест фильтра команд"""
        filter_obj = CommandFilter("start")
        user = User(id=123)
        chat = Chat(id=456, type="private")
        message = Message(
            message_id=1,
            date=datetime.now(),
            chat=chat,
            from_user=user,
            text="/start"
        )
        update = Update(update_id=1, message=message)
        
        result = await filter_obj.check(update)
        assert result is True


class TestRouter:
    """Тесты для роутера"""
    
    def test_router_creation(self):
        """Тест создания роутера"""
        router = Router("test_router")
        assert router.name == "test_router"
        assert len(router.handlers) == 0
    
    def test_add_handler(self):
        """Тест добавления обработчика"""
        router = Router()
        
        async def test_handler(message):
            return "test"
        
        handler = MessageHandler(test_handler)
        router.add_handler(handler)
        
        assert len(router.handlers) == 1
    
    @pytest.mark.asyncio
    async def test_router_handle(self):
        """Тест обработки через роутер"""
        router = Router()
        
        async def test_handler(message):
            return "handled"
        
        handler = MessageHandler(test_handler)
        router.add_handler(handler)
        
        user = User(id=123)
        chat = Chat(id=456, type="private")
        message = Message(
            message_id=1,
            date=datetime.now(),
            chat=chat,
            from_user=user,
            text="test"
        )
        update = Update(update_id=1, message=message)
        
        result = await router.handle(update)
        assert result == "handled"


class TestDialogManager:
    """Тесты для менеджера диалогов"""
    
    def test_session_creation(self):
        """Тест создания сессии"""
        manager = DialogManager()
        session = manager.get_session(123)
        
        assert session.user_id == 123
        assert session.state == DialogState.START
    
    def test_state_management(self):
        """Тест управления состояниями"""
        manager = DialogManager()
        manager.set_state(123, DialogState.CHOOSE_TYPE)
        
        state = manager.get_state(123)
        assert state == DialogState.CHOOSE_TYPE
    
    def test_config_update(self):
        """Тест обновления конфигурации"""
        manager = DialogManager()
        manager.update_config(123, name="Test Bot", description="Test Description")
        
        config = manager.get_config(123)
        assert config.name == "Test Bot"
        assert config.description == "Test Description"


class TestBotConfig:
    """Тесты для конфигурации бота"""
    
    def test_config_creation(self):
        """Тест создания конфигурации"""
        config = BotConfig(
            name="Test Bot",
            description="Test Description",
            bot_type=BotType.SIMPLE
        )
        
        assert config.name == "Test Bot"
        assert config.description == "Test Description"
        assert config.bot_type == BotType.SIMPLE
    
    def test_config_to_dict(self):
        """Тест преобразования в словарь"""
        config = BotConfig(
            name="Test Bot",
            description="Test Description",
            bot_type=BotType.SIMPLE
        )
        
        config_dict = config.to_dict()
        assert config_dict["name"] == "Test Bot"
        assert config_dict["bot_type"] == "simple"


if __name__ == "__main__":
    pytest.main([__file__])
