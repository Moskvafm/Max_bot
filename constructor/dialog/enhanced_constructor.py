"""
Расширенный конструктор ботов с полной настройкой
"""

import asyncio
from typing import Dict, Any, Optional, List
from max_bot import Dispatcher
from max_bot.filters.base import command, text
from max_bot.core.types import Message

from .state import DialogManager, DialogState, BotType, BotConfig
from .validator import BotValidator
from ..templates.bot_templates import BotTemplates
from ..generator.code_generator import CodeGenerator


class EnhancedConstructorBot:
    """Расширенный бот-конструктор с полной настройкой"""
    
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
🤖 Добро пожаловать в MAX Bot Constructor Pro!

Я помогу вам создать собственного бота с полной настройкой.

Доступные команды:
/start - Начать создание бота
/create - Создать нового бота
/customize - Настроить существующий бот
/help - Справка
/cancel - Отменить создание
/status - Статус создания
/preview - Предпросмотр бота

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
        
        @self.dp.message_handler(command("customize"))
        async def customize_command(message: Message):
            """Настройка существующего бота"""
            user_id = message.from_user.id
            config = self.dialog_manager.get_config(user_id)
            
            if not config.name:
                await message.answer("❌ Сначала создайте бота с помощью /create")
                return
            
            await self._show_customization_menu(message)
        
        @self.dp.message_handler(command("preview"))
        async def preview_command(message: Message):
            """Предпросмотр бота"""
            user_id = message.from_user.id
            config = self.dialog_manager.get_config(user_id)
            
            if not config.name:
                await message.answer("❌ Сначала создайте бота с помощью /create")
                return
            
            await self._show_preview(message, config)
        
        @self.dp.message_handler(command("help"))
        async def help_command(message: Message):
            """Расширенная справка"""
            help_text = """
📖 Справка по MAX Bot Constructor Pro

Этот бот поможет вам создать собственного бота для MAX с полной настройкой.

Процесс создания:
1. Выберите тип бота
2. Укажите имя и описание
3. Настройте команды и ответы
4. Предпросмотр и тестирование
5. Получите готовый код

Команды:
/start - Начать работу
/create - Создать нового бота
/customize - Настроить существующий бот
/preview - Предпросмотр бота
/help - Эта справка
/cancel - Отменить создание
/status - Статус текущего создания

Возможности:
✅ 5 готовых шаблонов
✅ Настройка команд
✅ Редактирование ответов
✅ Предпросмотр бота
✅ Валидация данных
✅ Генерация кода
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
            if config.responses:
                status_text += f"Ответов: {len(config.responses)}\n"
            
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
            elif state == DialogState.CUSTOMIZE_COMMANDS:
                await self._handle_command_customization(message, text)
            elif state == DialogState.CUSTOMIZE_RESPONSES:
                await self._handle_response_customization(message, text)
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
        
        # Показываем меню настройки
        await self._show_customization_menu(message)
    
    async def _show_customization_menu(self, message: Message):
        """Показать меню настройки"""
        user_id = message.from_user.id
        config = self.dialog_manager.get_config(user_id)
        
        menu_text = f"🔧 Настройка бота '{config.name}'\n\n"
        menu_text += "Выберите что хотите настроить:\n\n"
        menu_text += "1. 📝 Команды бота\n"
        menu_text += "2. 💬 Ответы бота\n"
        menu_text += "3. 👀 Предпросмотр\n"
        menu_text += "4. ✅ Завершить создание\n\n"
        menu_text += "Отправьте номер (1-4):"
        
        self.dialog_manager.set_state(user_id, DialogState.COMMANDS)
        await message.answer(menu_text)
    
    async def _handle_commands_input(self, message: Message, text: str):
        """Обработка выбора в меню настройки"""
        user_id = message.from_user.id
        
        try:
            choice = int(text)
            if choice == 1:
                await self._show_commands_editor(message)
            elif choice == 2:
                await self._show_responses_editor(message)
            elif choice == 3:
                config = self.dialog_manager.get_config(user_id)
                await self._show_preview(message, config)
            elif choice == 4:
                await self._show_confirmation(message)
            else:
                await message.answer("❌ Выберите от 1 до 4:")
        except ValueError:
            await message.answer("❌ Пожалуйста, введите число от 1 до 4:")
    
    async def _show_commands_editor(self, message: Message):
        """Показать редактор команд"""
        user_id = message.from_user.id
        config = self.dialog_manager.get_config(user_id)
        
        commands_text = "📝 Текущие команды бота:\n\n"
        
        if config.commands:
            for i, cmd in enumerate(config.commands, 1):
                commands_text += f"{i}. /{cmd['command']} - {cmd['description']}\n"
        else:
            commands_text += "Нет команд\n"
        
        commands_text += "\nДля добавления команды отправьте в формате:\n"
        commands_text += "команда:описание\n"
        commands_text += "Например: help:Показать справку\n\n"
        commands_text += "Для удаления команды отправьте: удалить НОМЕР\n"
        commands_text += "Для возврата отправьте: назад"
        
        self.dialog_manager.set_state(user_id, DialogState.CUSTOMIZE_COMMANDS)
        await message.answer(commands_text)
    
    async def _handle_command_customization(self, message: Message, text: str):
        """Обработка настройки команд"""
        user_id = message.from_user.id
        config = self.dialog_manager.get_config(user_id)
        
        if text.lower() == "назад":
            await self._show_customization_menu(message)
            return
        
        if text.lower().startswith("удалить"):
            try:
                parts = text.split()
                if len(parts) == 2:
                    index = int(parts[1]) - 1
                    if 0 <= index < len(config.commands):
                        del config.commands[index]
                        await message.answer("✅ Команда удалена!")
                        await self._show_commands_editor(message)
                    else:
                        await message.answer("❌ Неверный номер команды")
                else:
                    await message.answer("❌ Используйте формат: удалить НОМЕР")
            except ValueError:
                await message.answer("❌ Неверный номер")
            return
        
        if ":" in text:
            try:
                command_name, description = text.split(":", 1)
                command_name = command_name.strip()
                description = description.strip()
                
                if command_name and description:
                    # Проверяем на дубликаты
                    for cmd in config.commands:
                        if cmd["command"] == command_name:
                            await message.answer("❌ Команда уже существует")
                            return
                    
                    config.commands.append({
                        "command": command_name,
                        "description": description
                    })
                    await message.answer("✅ Команда добавлена!")
                    await self._show_commands_editor(message)
                else:
                    await message.answer("❌ Имя команды и описание не могут быть пустыми")
            except Exception:
                await message.answer("❌ Используйте формат: команда:описание")
        else:
            await message.answer("❌ Используйте формат: команда:описание")
    
    async def _show_responses_editor(self, message: Message):
        """Показать редактор ответов"""
        user_id = message.from_user.id
        config = self.dialog_manager.get_config(user_id)
        
        responses_text = "💬 Текущие ответы бота:\n\n"
        
        if config.responses:
            for key, response in config.responses.items():
                responses_text += f"'{key}': {response[:50]}...\n"
        else:
            responses_text += "Нет ответов\n"
        
        responses_text += "\nДля добавления ответа отправьте в формате:\n"
        responses_text += "ключ:ответ\n"
        responses_text += "Например: start:Привет! Я бот\n\n"
        responses_text += "Для удаления ответа отправьте: удалить КЛЮЧ\n"
        responses_text += "Для возврата отправьте: назад"
        
        self.dialog_manager.set_state(user_id, DialogState.CUSTOMIZE_RESPONSES)
        await message.answer(responses_text)
    
    async def _handle_response_customization(self, message: Message, text: str):
        """Обработка настройки ответов"""
        user_id = message.from_user.id
        config = self.dialog_manager.get_config(user_id)
        
        if text.lower() == "назад":
            await self._show_customization_menu(message)
            return
        
        if text.lower().startswith("удалить"):
            try:
                parts = text.split(" ", 1)
                if len(parts) == 2:
                    key = parts[1].strip()
                    if key in config.responses:
                        del config.responses[key]
                        await message.answer("✅ Ответ удален!")
                        await self._show_responses_editor(message)
                    else:
                        await message.answer("❌ Ключ не найден")
                else:
                    await message.answer("❌ Используйте формат: удалить КЛЮЧ")
            except Exception:
                await message.answer("❌ Ошибка при удалении")
            return
        
        if ":" in text:
            try:
                key, response = text.split(":", 1)
                key = key.strip()
                response = response.strip()
                
                if key and response:
                    config.responses[key] = response
                    await message.answer("✅ Ответ добавлен!")
                    await self._show_responses_editor(message)
                else:
                    await message.answer("❌ Ключ и ответ не могут быть пустыми")
            except Exception:
                await message.answer("❌ Используйте формат: ключ:ответ")
        else:
            await message.answer("❌ Используйте формат: ключ:ответ")
    
    async def _show_preview(self, message: Message, config: BotConfig):
        """Показать предпросмотр бота"""
        preview_text = f"👀 Предпросмотр бота '{config.name}'\n\n"
        preview_text += f"📝 Описание: {config.description}\n"
        preview_text += f"🏷️ Тип: {config.bot_type.value}\n\n"
        
        preview_text += "📋 Команды:\n"
        if config.commands:
            for cmd in config.commands:
                preview_text += f"• /{cmd['command']} - {cmd['description']}\n"
        else:
            preview_text += "Нет команд\n"
        
        preview_text += "\n💬 Ответы:\n"
        if config.responses:
            for key, response in list(config.responses.items())[:5]:  # Показываем первые 5
                preview_text += f"• '{key}': {response[:30]}...\n"
            if len(config.responses) > 5:
                preview_text += f"... и еще {len(config.responses) - 5} ответов\n"
        else:
            preview_text += "Нет ответов\n"
        
        await message.answer(preview_text)
    
    async def _show_confirmation(self, message: Message):
        """Показать подтверждение"""
        user_id = message.from_user.id
        config = self.dialog_manager.get_config(user_id)
        
        confirm_text = f"📋 Подтвердите создание бота:\n\n"
        confirm_text += f"Имя: {config.name}\n"
        confirm_text += f"Описание: {config.description}\n"
        confirm_text += f"Тип: {config.bot_type.value}\n"
        confirm_text += f"Команд: {len(config.commands)}\n"
        confirm_text += f"Ответов: {len(config.responses)}\n\n"
        confirm_text += f"Создать бота? (да/нет)"
        
        self.dialog_manager.set_state(user_id, DialogState.CONFIRM)
        await message.answer(confirm_text)
    
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
                               f"4. Запустите: python bot.py\n\n"
                               f"🎉 Ваш бот готов к использованию!")
            
            self.dialog_manager.set_state(user_id, DialogState.FINISHED)
        elif text.lower() in ['нет', 'no', 'n', '0']:
            self.dialog_manager.reset_session(user_id)
            await message.answer("❌ Создание отменено. Используйте /start для начала заново.")
        else:
            await message.answer("Пожалуйста, ответьте 'да' или 'нет':")
    
    def run(self):
        """Запуск расширенного бота-конструктора"""
        self.dp.run()
