#!/usr/bin/env python3
"""
Эмулятор командной оболочки UNIX-подобной ОС
Этап 5: Дополнительные команды
"""

import getpass
import socket
import shlex
import sys
from typing import List, Optional
from pathlib import Path
from config import Config, parse_arguments, validate_config
from vfs import VirtualFileSystem


class ShellEmulator:
    """Класс эмулятора командной оболочки"""

    def __init__(self, config: Config):
        """
        Инициализация эмулятора
        
        Args:
            config: Объект конфигурации
        """
        self.config = config
        self.running = True
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.script_mode = False
        
        self.vfs = VirtualFileSystem()
        self.vfs_loaded = False
        
        if config.vfs_path:
            self.vfs_loaded = self.vfs.load_from_zip(config.vfs_path)
        elif config.vfs_base64:
            self.vfs_loaded = self.vfs.load_from_base64(config.vfs_base64)
        
        self.commands = {
            'ls': self.cmd_ls,
            'cd': self.cmd_cd,
            'pwd': self.cmd_pwd,
            'cat': self.cmd_cat,
            'tree': self.cmd_tree,
            'find': self.cmd_find,
            'chown': self.cmd_chown,
            'rm': self.cmd_rm,
            'vfs-info': self.cmd_vfs_info,
            'exit': self.cmd_exit,
        }

    def get_prompt(self) -> str:
        """Формирует приглашение к вводу"""
        if self.vfs_loaded:
            current_path = self.vfs.get_current_path()
        else:
            current_path = "~"
        
        return f"{self.username}@{self.hostname}:{current_path}$ "

    def parse_command(self, input_line: str) -> tuple[Optional[str], List[str]]:
        """Парсит введенную команду"""
        try:
            tokens = shlex.split(input_line)
            
            if not tokens:
                return None, []
            
            command = tokens[0]
            args = tokens[1:]
            
            return command, args
            
        except ValueError as e:
            print(f"Ошибка парсинга: {e}")
            return None, []

    def execute_command(self, command: str, args: List[str]) -> bool:
        """Выполняет команду с заданными аргументами"""
        if command in self.commands:
            try:
                self.commands[command](args)
                return True
            except Exception as e:
                print(f"Ошибка выполнения команды '{command}': {e}")
                if self.config.debug:
                    import traceback
                    traceback.print_exc()
                return False
        else:
            print(f"Ошибка: команда не найдена: {command}")
            return False

    def execute_script(self, script_path: Path) -> bool:
        """Выполняет стартовый скрипт"""
        print(f"\n{'='*60}")
        print(f"Выполнение стартового скрипта: {script_path}")
        print(f"{'='*60}\n")

        self.script_mode = True
        line_number = 0
        error_occurred = False

        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line_number += 1
                    line = line.rstrip('\n\r')
                    
                    if not line.strip():
                        continue
                    
                    if line.strip().startswith('#'):
                        if self.config.debug:
                            print(f"[Комментарий] {line}")
                        continue
                    
                    print(f"{self.get_prompt()}{line}")
                    
                    command, args = self.parse_command(line)
                    
                    if command:
                        success = self.execute_command(command, args)
                        if not success:
                            error_occurred = True
                            print(f"Ошибка в скрипте на строке {line_number}: {line}")
                            if not self.config.debug:
                                break
                    
                    print()

        except FileNotFoundError:
            print(f"Ошибка: файл скрипта не найден: {script_path}")
            error_occurred = True
        except PermissionError:
            print(f"Ошибка: нет прав на чтение файла: {script_path}")
            error_occurred = True
        except UnicodeDecodeError:
            print(f"Ошибка: не удалось декодировать файл: {script_path}")
            error_occurred = True
        except Exception as e:
            print(f"Непредвиденная ошибка при выполнении скрипта: {e}")
            if self.config.debug:
                import traceback
                traceback.print_exc()
            error_occurred = True
        finally:
            self.script_mode = False

        print(f"{'='*60}")
        if error_occurred:
            print(f"Скрипт завершен с ошибками")
        else:
            print(f"Скрипт выполнен успешно")
        print(f"{'='*60}\n")

        return not error_occurred

    def cmd_ls(self, args: List[str]) -> None:
        """Команда ls: список файлов и директорий"""
        if not self.vfs_loaded:
            print("ls: VFS не загружена")
            return
        
        show_all = False
        long_format = False
        paths = []
        
        for arg in args:
            if arg.startswith('-'):
                if 'a' in arg:
                    show_all = True
                if 'l' in arg:
                    long_format = True
            else:
                paths.append(arg)
        
        if not paths:
            paths = [""]
        
        for i, path in enumerate(paths):
            if len(paths) > 1 and i > 0:
                print()
            
            if len(paths) > 1:
                print(f"{path}:")
            
            lines = self.vfs.list_directory(path, show_all, long_format)
            for line in lines:
                print(line)

    def cmd_cd(self, args: List[str]) -> None:
        """Команда cd: смена директории"""
        if not self.vfs_loaded:
            print("cd: VFS не загружена")
            return
        
        if len(args) == 0:
            self.vfs.change_directory("/")
        elif len(args) == 1:
            self.vfs.change_directory(args[0])
        else:
            print("cd: слишком много аргументов")

    def cmd_pwd(self, args: List[str]) -> None:
        """Команда pwd: вывод текущего пути"""
        if not self.vfs_loaded:
            print("~")
            return
        
        print(self.vfs.get_current_path())

    def cmd_cat(self, args: List[str]) -> None:
        """Команда cat: вывод содержимого файла"""
        if not self.vfs_loaded:
            print("cat: VFS не загружена")
            return
        
        if len(args) == 0:
            print("cat: отсутствует операнд")
            return
        
        for i, path in enumerate(args):
            if len(args) > 1 and i > 0:
                print()
            
            content = self.vfs.cat(path)
            if content:
                print(content)

    def cmd_tree(self, args: List[str]) -> None:
        """Команда tree: дерево файлов и директорий"""
        if not self.vfs_loaded:
            print("tree: VFS не загружена")
            return
        
        lines = self.vfs.get_tree()
        for line in lines:
            print(line)

    def cmd_find(self, args: List[str]) -> None:
        """Команда find: поиск файлов по имени"""
        if not self.vfs_loaded:
            print("find: VFS не загружена")
            return
        
        if len(args) == 0:
            print("find: отсутствует аргумент для поиска")
            return
        
        name = args[0]
        results = self.vfs.find(name)
        
        if results:
            for path in results:
                print(path)
        else:
            print(f"find: '{name}' не найдено")

    def cmd_chown(self, args: List[str]) -> None:
        """
        Команда chown: изменение владельца файла
        Использование: chown [-R] owner[:group] file
        """
        if not self.vfs_loaded:
            print("chown: VFS не загружена")
            return
        
        if len(args) == 0:
            print("chown: отсутствуют операнды")
            print("Использование: chown [-R] owner[:group] file")
            return
        
        recursive = False
        owner_group = None
        path = None
        
        for arg in args:
            if arg == '-R' or arg == '-r':
                recursive = True
            elif owner_group is None:
                owner_group = arg
            else:
                path = arg
        
        if owner_group is None or path is None:
            print("chown: неверный формат")
            print("Использование: chown [-R] owner[:group] file")
            return
        
        if ':' in owner_group:
            parts = owner_group.split(':', 1)
            owner = parts[0]
            group = parts[1]
        else:
            owner = owner_group
            group = None
        
        self.vfs.chown(path, owner, group, recursive)

    def cmd_rm(self, args: List[str]) -> None:
        """
        Команда rm: удаление файлов и директорий
        Использование: rm [-rf] file...
        """
        if not self.vfs_loaded:
            print("rm: VFS не загружена")
            return
        
        if len(args) == 0:
            print("rm: отсутствует операнд")
            print("Использование: rm [-rf] file...")
            return
        
        recursive = False
        force = False
        paths = []
        
        for arg in args:
            if arg.startswith('-'):
                if 'r' in arg or 'R' in arg:
                    recursive = True
                if 'f' in arg:
                    force = True
            else:
                paths.append(arg)
        
        if not paths:
            print("rm: отсутствует операнд")
            return
        
        for path in paths:
            self.vfs.remove(path, recursive, force)

    def cmd_vfs_info(self, args: List[str]) -> None:
        """Команда vfs-info: информация о VFS"""
        if not self.vfs_loaded:
            print("VFS не загружена")
            return
        
        stats = self.vfs.get_stats()
        
        print("Информация о виртуальной файловой системе:")
        print(f"  Источник: {self.vfs.loaded_from}")
        print(f"  Файлов: {stats['files']}")
        print(f"  Директорий: {stats['directories']}")
        print(f"  Общий размер: {stats['total_size']} байт ({stats['total_size'] / 1024:.2f} КБ)")
        print(f"  Текущая директория: {self.vfs.get_current_path()}")

    def cmd_exit(self, args: List[str]) -> None:
        """Команда выхода из эмулятора"""
        print("Выход из эмулятора...")
        self.running = False

    def print_debug_info(self) -> None:
        """Выводит отладочную информацию при запуске"""
        print("=" * 60)
        print("ОТЛАДОЧНАЯ ИНФОРМАЦИЯ")
        print("=" * 60)
        print(self.config)
        print(f"  Пользователь: {self.username}")
        print(f"  Хост: {self.hostname}")
        print(f"  VFS загружена: {self.vfs_loaded}")
        if self.vfs_loaded:
            stats = self.vfs.get_stats()
            print(f"  VFS файлов: {stats['files']}")
            print(f"  VFS директорий: {stats['directories']}")
        print(f"  Доступные команды: {', '.join(sorted(self.commands.keys()))}")
        print("=" * 60)
        print()

    def run(self) -> None:
        """Запускает главный цикл REPL"""
        if self.config.debug:
            self.print_debug_info()

        print("=" * 60)
        print("Эмулятор командной оболочки UNIX")
        print("Этап 5: Дополнительные команды")
        print("=" * 60)
        print("Доступные команды: ls, cd, pwd, cat, tree, find, chown, rm, vfs-info, exit")
        print("Для выхода введите 'exit' или нажмите Ctrl+D")
        print("=" * 60)
        print()

        if self.config.startup_script:
            script_success = self.execute_script(self.config.startup_script)
            if not script_success and not self.config.debug:
                print("Выполнение прервано из-за ошибок в стартовом скрипте")
                return

        while self.running:
            try:
                user_input = input(self.get_prompt()).strip()
                
                if not user_input:
                    continue
                
                command, args = self.parse_command(user_input)
                
                if command:
                    self.execute_command(command, args)
                    
            except KeyboardInterrupt:
                print("\nИспользуйте 'exit' для выхода")
                continue
                
            except EOFError:
                print("\nВыход из эмулятора...")
                break


def main():
    """Точка входа в приложение"""
    config = parse_arguments()
    
    if not validate_config(config):
        sys.exit(1)
    
    emulator = ShellEmulator(config)
    emulator.run()


if __name__ == "__main__":
    main()