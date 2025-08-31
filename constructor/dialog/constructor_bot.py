"""
Основной бот-конструктор с диалоговым интерфейсом
"""

import asyncio
from typing import Dict, Any, Optional
from max_bot import Dispatcher
from max_bot.filters.base import command, text
from max_bot.core.types import Message

from .state import DialogManager, DialogState, BotType, BotConfig
from .validator import BotValidator
from ..templates.bot_templates import BotTemplates
from ..generator.code_generator import CodeGenerator


class ConstructorBot:
    """Бот-конструктор для создания других ботов"""
    
    def __init__(self, token: str):
        self.dp = Dispatcher(token)
        self.dialog_manager = DialogManager()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Настройка обработчиков"""
        
        @self.dp.message_handler(command("start"))
        async def start_command(message: Message):
            """Начало работы с конструктором"""
            user_id = message.from_user.id
            self.dialog_manager.reset_session(user_id)
            self.dialog_manager.set_state(user_id, DialogState.START)
            
            welcome_text = """
🤖 Добро пожаловать в MAX Bot Constructor!

Я помогу вам создать собственного бота без программирования.

Доступные команды:
/start - Начать создание бота
/help - Справка
/cancel - Отменить создание
/status - Статус создания

Начнем создание бота? Отправьте /create
            """
            await message.answer(welcome_text)
        
        @self.dp.message_handler(command("create"))
        async def create_command(message: Message):
            """Начало создания бота"""
            user_id = message.from_user.id
            self.dialog_manager.set_state(user_id, DialogState.CHOOSE_TYPE)
            
            templates = BotTemplates.get_all_templates()
            choose_text = "Выберите тип бота:\n\n"
            
            for i, (key, template) in enumerate(templates.items(), 1):
                choose_text += f"{i}. {template['name']}\n"
                choose_text += f"   {template['description']}\n\n"
            
            choose_text += "Отправьте номер типа бота (1-5):"
            await message.answer(choose_text)
        
        @self.dp.message_handler(command("help"))
        async def help_command(message: Message):
            """Справка"""
            help_text = """
📖 Справка по MAX Bot Constructor

Этот бот поможет вам создать собственного бота для MAX без навыков программирования.

Процесс создания:
1. Выберите тип бота
2. Укажите имя и описание
3. Настройте команды и ответы
4. Получите готовый код

Команды:
/start - Начать работу
/create - Создать нового бота
/help - Эта справка
/cancel - Отменить создание
/status - Статус текущего создания
            """
            await message.answer(help_text)
        
        @self.dp.message_handler(command("cancel"))
        async def cancel_command(message: Message):
            """Отмена создания"""
            user_id = message.from_user.id
            self.dialog_manager.reset_session(user_id)
            await message.answer("❌ Создание бота отменено. Используйте /start для начала заново.")
        
        @self.dp.message_handler(command("status"))
        async def status_command(message: Message):
            """Статус создания"""
            user_id = message.from_user.id
            state = self.dialog_manager.get_state(user_id)
            config = self.dialog_manager.get_config(user_id)
            
            status_text = f"📊 Статус создания бота:\n\n"
            status_text += f"Этап: {state.value}\n"
            
            if config.name:
                status_text += f"Имя: {config.name}\n"
            if config.description:
                status_text += f"Описание: {config.description}\n"
            if config.bot_type:
                status_text += f"Тип: {config.bot_type.value}\n"
            if config.commands:
                status_text += f"Команд: {len(config.commands)}\n"
            
            await message.answer(status_text)
        
        # Обработчики диалога
        @self.dp.message_handler()
        async def dialog_handler(message: Message):
            """Обработчик диалога"""
            user_id = message.from_user.id
            state = self.dialog_manager.get_state(user_id)
            text = message.text
            
            if state == DialogState.START:
                await message.answer("Используйте /create для начала создания бота")
                return
            
            if state == DialogState.CHOOSE_TYPE:
                await self._handle_type_selection(message, text)
            elif state == DialogState.BOT_NAME:
                await self._handle_name_input(message, text)
            elif state == DialogState.BOT_DESCRIPTION:
                await self._handle_description_input(message, text)
            elif state == DialogState.COMMANDS:
                await self._handle_commands_input(message, text)
            elif state == DialogState.RESPONSES:
                await self._handle_responses_input(message, text)
            elif state == DialogState.CONFIRM:
                await self._handle_confirmation(message, text)
    
    async def _handle_type_selection(self, message: Message, text: str):
        """Обработка выбора типа бота"""
        user_id = message.from_user.id
        
        try:
            choice = int(text)
            templates = list(BotTemplates.get_all_templates().keys())
            
            if 1 <= choice <= len(templates):
                bot_type_name = templates[choice - 1]
                bot_type = BotType(bot_type_name)
                
                # Применяем шаблон
                template = BotTemplates.get_template(bot_type)
                BotTemplates.apply_template(self.dialog_manager.get_config(user_id), template)
                
                self.dialog_manager.set_state(user_id, DialogState.BOT_NAME)
                await message.answer("Отлично! Теперь введите имя для вашего бота:")
            else:
                await message.answer("❌ Неверный номер. Выберите от 1 до 5:")
        except ValueError:
            await message.answer("❌ Пожалуйста, введите число от 1 до 5:")
    
    async def _handle_name_input(self, message: Message, text: str):
        """Обработка ввода имени"""
        user_id = message.from_user.id
        
        # Валидация имени
        is_valid, error = BotValidator.validate_name(text)
        if not is_valid:
            await message.answer(f"❌ {error}\nПопробуйте еще раз:")
            return
        
        # Сохраняем имя
        self.dialog_manager.update_config(user_id, name=text)
        self.dialog_manager.set_state(user_id, DialogState.BOT_DESCRIPTION)
        
        await message.answer("Отлично! Теперь введите описание бота:")
    
    async def _handle_description_input(self, message: Message, text: str):
        """Обработка ввода описания"""
        user_id = message.from_user.id
        
        # Валидация описания
        is_valid, error = BotValidator.validate_description(text)
        if not is_valid:
            await message.answer(f"❌ {error}\nПопробуйте еще раз:")
            return
        
        # Сохраняем описание
        self.dialog_manager.update_config(user_id, description=text)
        
        # Переходим к подтверждению
        await self._show_confirmation(message)
    
    async def _handle_commands_input(self, message: Message, text: str):
        """Обработка ввода команд (заглушка)"""
        await message.answer("Функция настройки команд будет добавлена позже.")
    
    async def _handle_responses_input(self, message: Message, text: str):
        """Обработка ввода ответов (заглушка)"""
        await message.answer("Функция настройки ответов будет добавлена позже.")
    
    async def _handle_confirmation(self, message: Message, text: str):
        """Обработка подтверждения"""
        user_id = message.from_user.id
        
        if text.lower() in ['да', 'yes', 'y', '1']:
            # Генерируем код
            config = self.dialog_manager.get_config(user_id)
            output_dir = CodeGenerator.generate_project_structure(config)
            
            await message.answer(f"✅ Бот успешно создан!\n\n"
                               f"Файлы сохранены в папке: {output_dir}\n\n"
                               f"Для запуска бота:\n"
                               f"1. Перейдите в папку {output_dir}\n"
                               f"2. Установите зависимости: pip install -r requirements.txt\n"
                               f"3. Настройте токен в bot.py\n"
                               f"4. Запустите: python bot.py")
            
            self.dialog_manager.set_state(user_id, DialogState.FINISHED)
        elif text.lower() in ['нет', 'no', 'n', '0']:
            self.dialog_manager.reset_session(user_id)
            await message.answer("❌ Создание отменено. Используйте /start для начала заново.")
        else:
            await message.answer("Пожалуйста, ответьте 'да' или 'нет':")
    
    async def _show_confirmation(self, message: Message):
        """Показать подтверждение"""
        user_id = message.from_user.id
        config = self.dialog_manager.get_config(user_id)
        
        confirm_text = f"📋 Подтвердите создание бота:\n\n"
        confirm_text += f"Имя: {config.name}\n"
        confirm_text += f"Описание: {config.description}\n"
        confirm_text += f"Тип: {config.bot_type.value}\n"
        confirm_text += f"Команд: {len(config.commands)}\n\n"
        confirm_text += f"Создать бота? (да/нет)"
        
        self.dialog_manager.set_state(user_id, DialogState.CONFIRM)
        await message.answer(confirm_text)
    
    def run(self):
        """Запуск бота-конструктора"""
        self.dp.run()
