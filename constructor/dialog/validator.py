"""
Валидация данных для конструктора ботов
"""

import re
from typing import Dict, List, Any, Tuple, Optional
from ..dialog.state import BotConfig, BotType


class ValidationError(Exception):
    """Ошибка валидации"""
    pass


class BotValidator:
    """Валидатор конфигурации бота"""
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, Optional[str]]:
        """Валидация имени бота"""
        if not name:
            return False, "Имя бота не может быть пустым"
        
        if len(name) < 2:
            return False, "Имя бота должно содержать минимум 2 символа"
        
        if len(name) > 50:
            return False, "Имя бота не может быть длиннее 50 символов"
        
        # Проверка на допустимые символы
        if not re.match(r'^[a-zA-Zа-яА-Я0-9\s\-_]+$', name):
            return False, "Имя бота содержит недопустимые символы"
        
        return True, None
    
    @staticmethod
    def validate_description(description: str) -> Tuple[bool, Optional[str]]:
        """Валидация описания бота"""
        if not description:
            return False, "Описание бота не может быть пустым"
        
        if len(description) < 10:
            return False, "Описание должно содержать минимум 10 символов"
        
        if len(description) > 500:
            return False, "Описание не может быть длиннее 500 символов"
        
        return True, None
    
    @staticmethod
    def validate_commands(commands: List[Dict[str, str]]) -> Tuple[bool, Optional[str]]:
        """Валидация команд"""
        if not commands:
            return True, None  # Команды не обязательны
        
        for i, cmd in enumerate(commands):
            # Проверка структуры команды
            if not isinstance(cmd, dict):
                return False, f"Команда {i+1} должна быть словарем"
            
            if "command" not in cmd:
                return False, f"Команда {i+1} должна содержать поле 'command'"
            
            if "description" not in cmd:
                return False, f"Команда {i+1} должна содержать поле 'description'"
            
            # Валидация названия команды
            command_name = cmd["command"]
            if not command_name:
                return False, f"Название команды {i+1} не может быть пустым"
            
            if not re.match(r'^[a-z0-9_]+$', command_name):
                return False, f"Название команды {i+1} содержит недопустимые символы"
            
            if len(command_name) > 20:
                return False, f"Название команды {i+1} не может быть длиннее 20 символов"
            
            # Валидация описания команды
            description = cmd["description"]
            if not description:
                return False, f"Описание команды {i+1} не может быть пустым"
            
            if len(description) > 100:
                return False, f"Описание команды {i+1} не может быть длиннее 100 символов"
        
        # Проверка на дубликаты команд
        command_names = [cmd["command"] for cmd in commands]
        if len(command_names) != len(set(command_names)):
            return False, "Обнаружены дублирующиеся команды"
        
        return True, None
    
    @staticmethod
    def validate_responses(responses: Dict[str, str]) -> Tuple[bool, Optional[str]]:
        """Валидация ответов"""
        if not responses:
            return True, None  # Ответы не обязательны
        
        for key, response in responses.items():
            if not key:
                return False, "Ключ ответа не может быть пустым"
            
            if not response:
                return False, f"Ответ для ключа '{key}' не может быть пустым"
            
            if len(response) > 1000:
                return False, f"Ответ для ключа '{key}' не может быть длиннее 1000 символов"
        
        return True, None
    
    @staticmethod
    def validate_settings(settings: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Валидация настроек"""
        if not settings:
            return True, None  # Настройки не обязательны
        
        # Проверка типов настроек
        for key, value in settings.items():
            if not isinstance(key, str):
                return False, "Ключи настроек должны быть строками"
            
            if not key:
                return False, "Ключ настройки не может быть пустым"
            
            # Проверка допустимых типов значений
            if not isinstance(value, (str, int, float, bool, list, dict)):
                return False, f"Недопустимый тип значения для настройки '{key}'"
        
        return True, None
    
    @staticmethod
    def validate_config(config: BotConfig) -> Tuple[bool, List[str]]:
        """Полная валидация конфигурации"""
        errors = []
        
        # Валидация имени
        is_valid, error = BotValidator.validate_name(config.name)
        if not is_valid:
            errors.append(error)
        
        # Валидация описания
        is_valid, error = BotValidator.validate_description(config.description)
        if not is_valid:
            errors.append(error)
        
        # Валидация команд
        is_valid, error = BotValidator.validate_commands(config.commands)
        if not is_valid:
            errors.append(error)
        
        # Валидация ответов
        is_valid, error = BotValidator.validate_responses(config.responses)
        if not is_valid:
            errors.append(error)
        
        # Валидация настроек
        is_valid, error = BotValidator.validate_settings(config.settings)
        if not is_valid:
            errors.append(error)
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_step(step: str, data: Any) -> Tuple[bool, Optional[str]]:
        """Валидация конкретного шага"""
        validators = {
            "name": BotValidator.validate_name,
            "description": BotValidator.validate_description,
            "commands": BotValidator.validate_commands,
            "responses": BotValidator.validate_responses,
            "settings": BotValidator.validate_settings
        }
        
        if step not in validators:
            return True, None
        
        return validators[step](data)
