#!/usr/bin/env python3
"""
Модуль для работы с конфигурацией эмулятора
Версия 0.3.0 - добавлена поддержка VFS
"""

import argparse
import sys
from pathlib import Path
from typing import Optional


class Config:
    """Класс для хранения конфигурации эмулятора"""

    def __init__(self):
        """Инициализация конфигурации значениями по умолчанию"""
        self.vfs_path: Optional[Path] = None
        self.vfs_base64: Optional[str] = None
        self.startup_script: Optional[Path] = None
        self.debug: bool = False

    def __str__(self) -> str:
        """Строковое представление конфигурации"""
        vfs_info = "не указан"
        if self.vfs_path:
            vfs_info = str(self.vfs_path)
        elif self.vfs_base64:
            vfs_info = "base64 строка"
        
        return (
            f"Конфигурация эмулятора:\n"
            f"  VFS: {vfs_info}\n"
            f"  Стартовый скрипт: {self.startup_script or 'не указан'}\n"
            f"  Режим отладки: {self.debug}"
        )


def parse_arguments() -> Config:
    """
    Парсит аргументы командной строки и возвращает объект конфигурации
    
    Returns:
        Config: Объект конфигурации с заполненными параметрами
    """
    parser = argparse.ArgumentParser(
        description='Эмулятор командной оболочки UNIX с виртуальной файловой системой',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s
  %(prog)s --vfs tests/vfs_archives/minimal_vfs.zip
  %(prog)s --vfs tests/vfs_archives/complex_vfs.zip --startup tests/test_scripts/test_vfs_full.sh
  %(prog)s --vfs-base64 "UEsDBB..." --debug
        """
    )

    parser.add_argument(
        '--vfs',
        type=str,
        metavar='PATH',
        help='Путь к ZIP-архиву виртуальной файловой системы (VFS)'
    )

    parser.add_argument(
        '--vfs-base64',
        type=str,
        metavar='STRING',
        help='VFS в формате base64 (ZIP-архив закодированный в base64)'
    )

    parser.add_argument(
        '--startup',
        type=str,
        metavar='SCRIPT',
        help='Путь к стартовому скрипту для выполнения команд при запуске'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Включить режим отладки с выводом дополнительной информации'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.3.0 (Этап 3: VFS)'
    )

    args = parser.parse_args()

    # Создаем объект конфигурации
    config = Config()
    config.debug = args.debug

    # Проверяем взаимоисключающие параметры
    if args.vfs and args.vfs_base64:
        print("Ошибка: нельзя использовать --vfs и --vfs-base64 одновременно", file=sys.stderr)
        sys.exit(1)

    # Проверяем и устанавливаем путь к VFS
    if args.vfs:
        vfs_path = Path(args.vfs)
        if not vfs_path.exists():
            print(f"Ошибка: файл VFS не найден: {vfs_path}", file=sys.stderr)
            sys.exit(1)
        if not vfs_path.is_file():
            print(f"Ошибка: путь VFS не является файлом: {vfs_path}", file=sys.stderr)
            sys.exit(1)
        config.vfs_path = vfs_path

    # Устанавливаем base64 VFS
    if args.vfs_base64:
        config.vfs_base64 = args.vfs_base64

    # Проверяем и устанавливаем путь к стартовому скрипту
    if args.startup:
        startup_path = Path(args.startup)
        if not startup_path.exists():
            print(f"Ошибка: стартовый скрипт не найден: {startup_path}", file=sys.stderr)
            sys.exit(1)
        if not startup_path.is_file():
            print(f"Ошибка: путь к стартовому скрипту не является файлом: {startup_path}", file=sys.stderr)
            sys.exit(1)
        config.startup_script = startup_path

    return config


def validate_config(config: Config) -> bool:
    """
    Валидирует конфигурацию
    
    Args:
        config: Объект конфигурации для проверки
        
    Returns:
        bool: True если конфигурация валидна, иначе False
    """
    if config.vfs_path and not config.vfs_path.exists():
        print(f"Ошибка: VFS файл не существует: {config.vfs_path}", file=sys.stderr)
        return False

    if config.startup_script and not config.startup_script.exists():
        print(f"Ошибка: стартовый скрипт не существует: {config.startup_script}", file=sys.stderr)
        return False

    return True