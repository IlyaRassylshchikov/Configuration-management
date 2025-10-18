#!/usr/bin/env python3
"""
Автоматические тесты для эмулятора оболочки
Версия: 0.2.0 (Этап 2)
"""

import sys
import os
from pathlib import Path
from io import StringIO

# Добавляем родительскую директорию в путь для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))

from shell_emulator import ShellEmulator
from config import Config, parse_arguments


def test_parse_command():
    """Тест парсинга команд"""
    print("🧪 Тест: Парсинг команд")
    
    config = Config()
    emulator = ShellEmulator(config)
    
    # Тест 1: Простая команда
    cmd, args = emulator.parse_command("ls")
    assert cmd == "ls" and args == [], f"Ошибка: простая команда. Получено: {cmd}, {args}"
    
    # Тест 2: Команда с аргументами
    cmd, args = emulator.parse_command("ls -la /home")
    assert cmd == "ls" and args == ["-la", "/home"], f"Ошибка: команда с аргументами. Получено: {cmd}, {args}"
    
    # Тест 3: Аргументы в двойных кавычках
    cmd, args = emulator.parse_command('ls "my file.txt"')
    assert cmd == "ls" and args == ["my file.txt"], f"Ошибка: аргументы в кавычках. Получено: {cmd}, {args}"
    
    # Тест 4: Аргументы в одинарных кавычках
    cmd, args = emulator.parse_command("ls 'my file.txt'")
    assert cmd == "ls" and args == ["my file.txt"], f"Ошибка: одинарные кавычки. Получено: {cmd}, {args}"
    
    # Тест 5: Смешанные кавычки
    cmd, args = emulator.parse_command('ls "file 1" \'file 2\' file3')
    assert cmd == "ls" and args == ["file 1", "file 2", "file3"], f"Ошибка: смешанные кавычки. Получено: {cmd}, {args}"
    
    # Тест 6: Пустая строка
    cmd, args = emulator.parse_command("")
    assert cmd is None and args == [], f"Ошибка: пустая строка. Получено: {cmd}, {args}"
    
    print("   ✅ Все тесты парсинга пройдены!")


def test_commands_exist():
    """Тест наличия команд"""
    print("🧪 Тест: Наличие команд")
    
    config = Config()
    emulator = ShellEmulator(config)
    
    assert "ls" in emulator.commands, "Команда ls не найдена"
    assert "cd" in emulator.commands, "Команда cd не найдена"
    assert "exit" in emulator.commands, "Команда exit не найдена"
    
    print("   ✅ Все команды присутствуют!")


def test_prompt_format():
    """Тест формата приглашения"""
    print("🧪 Тест: Формат приглашения")
    
    config = Config()
    emulator = ShellEmulator(config)
    prompt = emulator.get_prompt()
    
    assert "@" in prompt, "В приглашении отсутствует @"
    assert ":" in prompt, "В приглашении отсутствует :"
    assert "$" in prompt, "В приглашении отсутствует $"
    assert "~" in prompt, "В приглашении отсутствует ~"
    
    print(f"   ✅ Формат приглашения корректен: {prompt}")


def test_config_creation():
    """Тест создания конфигурации"""
    print("🧪 Тест: Создание конфигурации")
    
    config = Config()
    
    assert config.vfs_path is None, "VFS путь должен быть None по умолчанию"
    assert config.startup_script is None, "Стартовый скрипт должен быть None по умолчанию"
    assert config.debug is False, "Режим отладки должен быть False по умолчанию"
    
    print("   ✅ Конфигурация создается корректно!")


def test_config_string_representation():
    """Тест строкового представления конфигурации"""
    print("🧪 Тест: Строковое представление конфигурации")
    
    config = Config()
    config_str = str(config)
    
    assert "Конфигурация эмулятора" in config_str, "Неверный формат строки конфигурации"
    assert "VFS путь" in config_str, "Отсутствует информация о VFS"
    assert "Стартовый скрипт" in config_str, "Отсутствует информация о скрипте"
    assert "Режим отладки" in config_str, "Отсутствует информация о режиме отладки"
    
    print("   ✅ Строковое представление корректно!")


def test_script_execution():
    """Тест выполнения скрипта"""
    print("🧪 Тест: Выполнение скрипта")
    
    # Создаем временный скрипт
    test_script_path = Path("tests/test_scripts/temp_test.sh")
    test_script_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(test_script_path, 'w', encoding='utf-8') as f:
        f.write("# Тестовый скрипт\n")
        f.write("ls\n")
        f.write("cd /home\n")
    
    try:
        config = Config()
        config.startup_script = test_script_path
        emulator = ShellEmulator(config)
        
        # Выполняем скрипт
        result = emulator.execute_script(test_script_path)
        
        assert result is True, "Скрипт должен выполниться успешно"
        
        print("   ✅ Выполнение скрипта работает корректно!")
        
    finally:
        # Удаляем временный файл
        if test_script_path.exists():
            test_script_path.unlink()


def test_execute_command():
    """Тест выполнения команд"""
    print("🧪 Тест: Выполнение команд")
    
    config = Config()
    emulator = ShellEmulator(config)
    
    # Перенаправляем stdout для проверки вывода
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        # Тест валидной команды
        result = emulator.execute_command("ls", ["-la"])
        output = sys.stdout.getvalue()
        
        assert result is True, "Команда ls должна выполниться успешно"
        assert "Команда: ls" in output, "В выводе должно быть имя команды"
        assert "['-la']" in output, "В выводе должны быть аргументы"
        
        # Очищаем буфер
        sys.stdout = StringIO()
        
        # Тест неизвестной команды
        result = emulator.execute_command("unknown", [])
        output = sys.stdout.getvalue()
        
        assert result is False, "Неизвестная команда должна вернуть False"
        assert "команда не найдена" in output, "Должно быть сообщение об ошибке"
        
        print("   ✅ Выполнение команд работает корректно!", file=old_stdout)
        
    finally:
        sys.stdout = old_stdout


def run_all_tests():
    """Запуск всех тестов"""
    print("=" * 60)
    print("Запуск автоматических тестов эмулятора оболочки")
    print("Версия: 0.2.0 (Этап 2: Конфигурация)")
    print("=" * 60)
    print()
    
    tests = [
        test_parse_command,
        test_commands_exist,
        test_prompt_format,
        test_config_creation,
        test_config_string_representation,
        test_script_execution,
        test_execute_command,
    ]
    
    failed_tests = []
    
    for test in tests:
        try:
            test()
            print()
        except AssertionError as e:
            print(f"   ❌ ТЕСТ ПРОВАЛЕН: {e}")
            print()
            failed_tests.append((test.__name__, str(e)))
        except Exception as e:
            print(f"   ❌ НЕПРЕДВИДЕННАЯ ОШИБКА: {e}")
            print()
            failed_tests.append((test.__name__, str(e)))
    
    print("=" * 60)
    if not failed_tests:
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("=" * 60)
        return 0
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ:")
        for test_name, error in failed_tests:
            print(f"   - {test_name}: {error}")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())