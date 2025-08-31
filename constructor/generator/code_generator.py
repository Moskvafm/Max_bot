"""
Генератор кода для создания ботов
"""

import os
from typing import Dict, List, Any
from ..dialog.state import BotConfig, BotType


class CodeGenerator:
    """Генератор кода ботов"""
    
    @staticmethod
    def generate_bot_code(config: BotConfig) -> str:
        """Генерация кода бота"""
        template = CodeGenerator._get_bot_template()
        
        # Заполняем шаблон данными
        code = template.format(
            bot_name=config.name,
            bot_description=config.description,
            imports=CodeGenerator._generate_imports(),
            handlers=CodeGenerator._generate_handlers(config),
            main_block=CodeGenerator._generate_main_block()
        )
        
        return code
    
    @staticmethod
    def _get_bot_template() -> str:
        """Шаблон кода бота"""
        return '''"""
{bot_name} - {bot_description}

Автоматически сгенерированный бот с помощью MAX Bot Constructor
"""

{imports}

# Создаем диспетчер
dp = Dispatcher("YOUR_BOT_TOKEN")

{handlers}

{main_block}
'''
    
    @staticmethod
    def _generate_imports() -> str:
        """Генерация импортов"""
        return '''from max_bot import Dispatcher
from max_bot.filters.base import command, text, callback_data
from max_bot.middleware.base import LoggingMiddleware, ThrottlingMiddleware

import asyncio
import logging'''
    
    @staticmethod
    def _generate_handlers(config: BotConfig) -> str:
        """Генерация обработчиков"""
        handlers = []
        
        # Добавляем обработчики команд
        for cmd in config.commands:
            command_name = cmd["command"]
            description = cmd["description"]
            
            handler_code = f'''
@dp.message_handler(command("{command_name}"))
async def {command_name}_command(message):
    """{description}"""
    response = config.responses.get("{command_name}", "Команда в разработке")
    await message.answer(response)'''
            
            handlers.append(handler_code)
        
        # Добавляем обработчик по умолчанию
        default_handler = '''
@dp.message_handler()
async def default_handler(message):
    """Обработчик по умолчанию"""
    response = config.responses.get("default", "Не понимаю эту команду. Используйте /help для справки.")
    await message.answer(response)'''
        
        handlers.append(default_handler)
        
        return '\n'.join(handlers)
    
    @staticmethod
    def _generate_main_block() -> str:
        """Генерация основного блока"""
        return '''if __name__ == "__main__":
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)
    
    # Добавляем middleware
    dp.add_middleware(LoggingMiddleware())
    dp.add_middleware(ThrottlingMiddleware(rate_limit=1.0))
    
    # Запускаем бота
    dp.run()'''
    
    @staticmethod
    def generate_config_file(config: BotConfig) -> str:
        """Генерация конфигурационного файла"""
        config_data = config.to_dict()
        
        config_code = f'''# Конфигурация бота {config.name}
BOT_CONFIG = {repr(config_data)}

# Настройки
BOT_SETTINGS = {repr(config.settings)}

# Команды
BOT_COMMANDS = {repr(config.commands)}

# Ответы
BOT_RESPONSES = {repr(config.responses)}
'''
        
        return config_code
    
    @staticmethod
    def generate_requirements() -> str:
        """Генерация requirements.txt"""
        return '''# Зависимости для MAX Bot
max-bot>=0.1.0
asyncio
logging
'''
    
    @staticmethod
    def generate_readme(config: BotConfig) -> str:
        """Генерация README.md"""
        return f'''# {config.name}

{config.description}

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте токен бота в файле `bot.py`

3. Запустите бота:
```bash
python bot.py
```

## Команды

{CodeGenerator._generate_commands_doc(config)}

## Автор

Создано с помощью MAX Bot Constructor
'''
    
    @staticmethod
    def _generate_commands_doc(config: BotConfig) -> str:
        """Генерация документации команд"""
        if not config.commands:
            return "Нет доступных команд"
        
        doc = ""
        for cmd in config.commands:
            doc += f"- `/{cmd['command']}` - {cmd['description']}\n"
        
        return doc
    
    @staticmethod
    def generate_project_structure(config: BotConfig, output_dir: str = "generated_bot"):
        """Генерация структуры проекта"""
        # Создаем директорию
        os.makedirs(output_dir, exist_ok=True)
        
        # Генерируем файлы
        files = {
            "bot.py": CodeGenerator.generate_bot_code(config),
            "config.py": CodeGenerator.generate_config_file(config),
            "requirements.txt": CodeGenerator.generate_requirements(),
            "README.md": CodeGenerator.generate_readme(config)
        }
        
        # Записываем файлы
        for filename, content in files.items():
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return output_dir
