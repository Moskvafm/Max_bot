"""
Основной бот-конструктор с диалоговым интерфейсом
"""

import asyncio
from typing import Dict, Any, Optional, List, Tuple
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
        
        # Переходим к настройке команд
        self.dialog_manager.set_state(user_id, DialogState.COMMANDS)
        await message.answer(
            "Теперь задайте команды бота.\n\n"
            "Формат: по одной на строку, 'command: Описание'.\n"
            "Примеры:\n"
            "/start: Начать работу с ботом\n"
            "/help: Показать справку\n\n"
            "Когда закончите, отправьте весь список одной строкой сообщением."
        )
    
    async def _handle_commands_input(self, message: Message, text: str):
        """Обработка ввода команд"""
        user_id = message.from_user.id
        commands, parse_error = self._parse_commands(text)
        if parse_error:
            await message.answer(f"❌ Ошибка в формате команд: {parse_error}\nПопробуйте еще раз.")
            return
        
        is_valid, error = BotValidator.validate_commands(commands)
        if not is_valid:
            await message.answer(f"❌ {error}\nПопробуйте еще раз.")
            return
        
        self.dialog_manager.update_config(user_id, commands=commands)
        self.dialog_manager.set_state(user_id, DialogState.RESPONSES)
        
        # Подсказка по ответам
        example_keys = [c["command"] for c in commands][:3]
        examples = "\n".join([f"{k}: Ответ для команды /{k}" for k in example_keys])
        await message.answer(
            "Команды сохранены. Теперь задайте ответы.\n\n"
            "Формат: 'ключ: текст ответа' по одному на строку.\n"
            "Ключи обычно совпадают с именами команд без '/'. Можно добавить 'default' для ответа по умолчанию.\n\n"
            f"Примеры:\n{examples}\ndefault: Не понимаю команду\n\n"
            "Отправьте список одним сообщением."
        )
    
    async def _handle_responses_input(self, message: Message, text: str):
        """Обработка ввода ответов"""
        user_id = message.from_user.id
        responses, parse_error = self._parse_responses(text)
        if parse_error:
            await message.answer(f"❌ Ошибка в формате ответов: {parse_error}\nПопробуйте еще раз.")
            return
        
        is_valid, error = BotValidator.validate_responses(responses)
        if not is_valid:
            await message.answer(f"❌ {error}\nПопробуйте еще раз.")
            return
        
        self.dialog_manager.update_config(user_id, responses=responses)
        await self._show_confirmation(message)

    def _parse_commands(self, raw: str) -> Tuple[List[Dict[str, str]], Optional[str]]:
        """Парсинг списка команд из текста пользователя."""
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        if not lines:
            return [], None
        commands: List[Dict[str, str]] = []
        for idx, line in enumerate(lines, 1):
            # Допускаем разделители ':' или '-' и возможный слеш в начале
            separator = ':' if ':' in line else ('-' if '-' in line else None)
            if not separator:
                return [], f"Строка {idx} должна содержать ':' или '-' как разделитель"
            name_part, desc_part = [p.strip() for p in line.split(separator, 1)]
            if name_part.startswith('/'):
                name_part = name_part[1:]
            if not name_part:
                return [], f"Пустое имя команды в строке {idx}"
            commands.append({"command": name_part.lower(), "description": desc_part})
        return commands, None

    def _parse_responses(self, raw: str) -> Tuple[Dict[str, str], Optional[str]]:
        """Парсинг словаря ответов из текста пользователя."""
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        if not lines:
            return {}, None
        responses: Dict[str, str] = {}
        for idx, line in enumerate(lines, 1):
            if ':' not in line:
                return {}, f"Строка {idx} должна содержать ':' как разделитель"
            key, value = [p.strip() for p in line.split(':', 1)]
            if key.startswith('/'):
                key = key[1:]
            if not key:
                return {}, f"Пустой ключ в строке {idx}"
            responses[key] = value
        return responses, None
    
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
