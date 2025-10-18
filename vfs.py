#!/usr/bin/env python3
"""
Модуль виртуальной файловой системы (VFS)
Работает полностью в памяти с ZIP-архивами
Этап 5: поддержка chown и rm
"""

import zipfile
import io
import base64
from pathlib import Path, PurePosixPath
from typing import Optional, List, Dict, Union
from datetime import datetime


class VFSNode:
    """Узел виртуальной файловой системы (файл или директория)"""
    
    def __init__(self, name: str, is_dir: bool = False, content: bytes = b"", 
                 parent: Optional['VFSNode'] = None, owner: str = "user", group: str = "group"):
        """
        Инициализация узла VFS
        
        Args:
            name: Имя файла или директории
            is_dir: True если это директория
            content: Содержимое файла (для файлов)
            parent: Родительская директория
            owner: Владелец файла
            group: Группа файла
        """
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.parent = parent
        self.owner = owner
        self.group = group
        self.children: Dict[str, 'VFSNode'] = {} if is_dir else None
        self.created = datetime.now()
        self.modified = datetime.now()
    
    def get_path(self) -> str:
        """Получить полный путь к узлу"""
        if self.parent is None:
            return "/"
        
        parts = []
        node = self
        while node.parent is not None:
            parts.append(node.name)
            node = node.parent
        
        if not parts:
            return "/"
        
        return "/" + "/".join(reversed(parts))
    
    def get_size(self) -> int:
        """Получить размер файла или директории"""
        if not self.is_dir:
            return len(self.content)
        
        total = 0
        for child in self.children.values():
            total += child.get_size()
        return total
    
    def __repr__(self) -> str:
        type_str = "DIR" if self.is_dir else "FILE"
        return f"<VFSNode {type_str} '{self.name}' owner={self.owner}:{self.group}>"


class VirtualFileSystem:
    """Виртуальная файловая система в памяти"""
    
    def __init__(self):
        """Инициализация пустой VFS"""
        self.root = VFSNode("/", is_dir=True, owner="root", group="root")
        self.current_dir = self.root
        self.loaded_from: Optional[Path] = None
    
    def load_from_zip(self, zip_path: Union[str, Path]) -> bool:
        """
        Загружает VFS из ZIP-архива в память
        
        Args:
            zip_path: Путь к ZIP-файлу
            
        Returns:
            bool: True если загрузка успешна
        """
        try:
            zip_path = Path(zip_path)
            
            if not zip_path.exists():
                print(f"Ошибка: ZIP-архив не найден: {zip_path}")
                return False
            
            with zipfile.ZipFile(zip_path, 'r') as zf:
                for info in zf.infolist():
                    if info.filename.startswith('__MACOSX') or info.filename.startswith('.'):
                        continue
                    
                    path = PurePosixPath(info.filename)
                    
                    if info.is_dir():
                        self._create_directory_recursive(str(path))
                    else:
                        content = zf.read(info.filename)
                        self._create_file_recursive(str(path), content)
            
            self.loaded_from = zip_path
            print(f"VFS успешно загружена из {zip_path}")
            return True
            
        except zipfile.BadZipFile:
            print(f"Ошибка: некорректный ZIP-архив: {zip_path}")
            return False
        except Exception as e:
            print(f"Ошибка загрузки VFS: {e}")
            return False
    
    def load_from_base64(self, b64_string: str) -> bool:
        """
        Загружает VFS из base64-строки
        
        Args:
            b64_string: ZIP-архив в формате base64
            
        Returns:
            bool: True если загрузка успешна
        """
        try:
            zip_data = base64.b64decode(b64_string)
            zip_buffer = io.BytesIO(zip_data)
            
            with zipfile.ZipFile(zip_buffer, 'r') as zf:
                for info in zf.infolist():
                    if info.filename.startswith('__MACOSX') or info.filename.startswith('.'):
                        continue
                    
                    path = PurePosixPath(info.filename)
                    
                    if info.is_dir():
                        self._create_directory_recursive(str(path))
                    else:
                        content = zf.read(info.filename)
                        self._create_file_recursive(str(path), content)
            
            self.loaded_from = "base64"
            print("VFS успешно загружена из base64")
            return True
            
        except Exception as e:
            print(f"Ошибка загрузки VFS из base64: {e}")
            return False
    
    def _create_directory_recursive(self, path: str) -> Optional[VFSNode]:
        """Создаёт директорию и все промежуточные директории"""
        path = path.strip('/')
        if not path:
            return self.root
        
        parts = path.split('/')
        current = self.root
        
        for part in parts:
            if not part:
                continue
            
            if part not in current.children:
                new_dir = VFSNode(part, is_dir=True, parent=current)
                current.children[part] = new_dir
            
            current = current.children[part]
        
        return current
    
    def _create_file_recursive(self, path: str, content: bytes) -> Optional[VFSNode]:
        """Создаёт файл и все промежуточные директории"""
        path = path.strip('/')
        parts = path.split('/')
        
        if len(parts) > 1:
            dir_path = '/'.join(parts[:-1])
            parent = self._create_directory_recursive(dir_path)
        else:
            parent = self.root
        
        filename = parts[-1]
        file_node = VFSNode(filename, is_dir=False, content=content, parent=parent)
        parent.children[filename] = file_node
        
        return file_node
    
    def resolve_path(self, path: str) -> Optional[VFSNode]:
        """
        Разрешает путь и возвращает соответствующий узел
        
        Args:
            path: Путь (абсолютный или относительный)
            
        Returns:
            VFSNode или None если путь не найден
        """
        if path in ('', '.'):
            return self.current_dir
        
        if path == '/':
            return self.root
        
        if path == '..':
            return self.current_dir.parent or self.current_dir
        
        if path.startswith('/'):
            current = self.root
            path = path[1:]
        else:
            current = self.current_dir
        
        if not path:
            return current
        
        parts = path.split('/')
        
        for part in parts:
            if not part or part == '.':
                continue
            
            if part == '..':
                current = current.parent or current
                continue
            
            if not current.is_dir:
                return None
            
            if part not in current.children:
                return None
            
            current = current.children[part]
        
        return current
    
    def change_directory(self, path: str) -> bool:
        """
        Меняет текущую директорию
        
        Args:
            path: Путь к новой директории
            
        Returns:
            bool: True если успешно
        """
        if not path:
            self.current_dir = self.root
            return True
        
        node = self.resolve_path(path)
        
        if node is None:
            print(f"cd: {path}: Нет такого файла или каталога")
            return False
        
        if not node.is_dir:
            print(f"cd: {path}: Не является каталогом")
            return False
        
        self.current_dir = node
        return True
    
    def list_directory(self, path: str = "", show_all: bool = False, 
                       long_format: bool = False) -> List[str]:
        """
        Выводит содержимое директории
        
        Args:
            path: Путь к директории (пустая строка = текущая)
            show_all: Показывать скрытые файлы
            long_format: Длинный формат вывода
            
        Returns:
            List[str]: Список строк для вывода
        """
        if path:
            node = self.resolve_path(path)
        else:
            node = self.current_dir
        
        if node is None:
            return [f"ls: невозможно получить доступ к '{path}': Нет такого файла или каталога"]
        
        if not node.is_dir:
            if long_format:
                return [self._format_long_entry(node)]
            else:
                return [node.name]
        
        result = []
        entries = sorted(node.children.values(), key=lambda x: x.name)
        
        if long_format:
            total_size = sum(e.get_size() for e in entries)
            result.append(f"total {len(entries)}")
            
            for entry in entries:
                result.append(self._format_long_entry(entry))
        else:
            for entry in entries:
                name = entry.name
                if entry.is_dir:
                    name += "/"
                result.append(name)
        
        return result
    
    def _format_long_entry(self, node: VFSNode) -> str:
        """Форматирует запись в длинном формате (как ls -l)"""
        perms = "d" if node.is_dir else "-"
        perms += "rwxr-xr-x"
        
        links = len(node.children) + 2 if node.is_dir else 1
        size = node.get_size()
        date_str = node.modified.strftime("%b %d %H:%M")
        
        name = node.name
        if node.is_dir:
            name += "/"
        
        return f"{perms} {links:3d} {node.owner:8s} {node.group:8s} {size:8d} {date_str} {name}"
    
    def get_current_path(self) -> str:
        """Возвращает текущий путь"""
        if self.current_dir == self.root:
            return "/"
        return self.current_dir.get_path()
    
    def cat(self, path: str) -> Optional[str]:
        """
        Выводит содержимое файла
        
        Args:
            path: Путь к файлу
            
        Returns:
            str: Содержимое файла или None
        """
        node = self.resolve_path(path)
        
        if node is None:
            print(f"cat: {path}: Нет такого файла или каталога")
            return None
        
        if node.is_dir:
            print(f"cat: {path}: Это каталог")
            return None
        
        try:
            return node.content.decode('utf-8')
        except UnicodeDecodeError:
            return f"[Бинарный файл, base64]:\n{base64.b64encode(node.content).decode('ascii')}"
    
    def get_tree(self, node: Optional[VFSNode] = None, prefix: str = "", 
                 is_last: bool = True) -> List[str]:
        """
        Получает дерево файлов и директорий
        
        Args:
            node: Начальный узел (None = текущая директория)
            prefix: Префикс для отступов
            is_last: Является ли узел последним в списке
            
        Returns:
            List[str]: Список строк дерева
        """
        if node is None:
            node = self.current_dir
        
        result = []
        
        if node != self.current_dir:
            connector = "└── " if is_last else "├── "
            name = node.name + ("/" if node.is_dir else "")
            result.append(prefix + connector + name)
        else:
            result.append(node.get_path())
        
        if node.is_dir and node.children:
            children = sorted(node.children.values(), key=lambda x: x.name)
            
            for i, child in enumerate(children):
                is_last_child = (i == len(children) - 1)
                
                if node == self.current_dir:
                    extension = ""
                else:
                    extension = "    " if is_last else "│   "
                
                result.extend(
                    self.get_tree(child, prefix + extension, is_last_child)
                )
        
        return result
    
    def find(self, name: str, node: Optional[VFSNode] = None) -> List[str]:
        """
        Ищет файлы по имени
        
        Args:
            name: Имя для поиска (поддерживает * в начале/конце)
            node: Начальный узел (None = текущая директория)
            
        Returns:
            List[str]: Список найденных путей
        """
        if node is None:
            node = self.current_dir
        
        results = []
        
        if self._name_matches(node.name, name):
            results.append(node.get_path())
        
        if node.is_dir:
            for child in node.children.values():
                results.extend(self.find(name, child))
        
        return results
    
    def _name_matches(self, filename: str, pattern: str) -> bool:
        """Проверяет соответствие имени файла паттерну"""
        if pattern == "*":
            return True
        
        if pattern.startswith("*") and pattern.endswith("*"):
            return pattern[1:-1] in filename
        
        if pattern.startswith("*"):
            return filename.endswith(pattern[1:])
        
        if pattern.endswith("*"):
            return filename.startswith(pattern[:-1])
        
        return filename == pattern
    
    def chown(self, path: str, owner: str, group: Optional[str] = None, recursive: bool = False) -> bool:
        """
        Меняет владельца файла или директории
        
        Args:
            path: Путь к файлу/директории
            owner: Новый владелец
            group: Новая группа (опционально)
            recursive: Рекурсивно для директорий
            
        Returns:
            bool: True если успешно
        """
        node = self.resolve_path(path)
        
        if node is None:
            print(f"chown: невозможно получить доступ к '{path}': Нет такого файла или каталога")
            return False
        
        self._chown_node(node, owner, group, recursive)
        return True
    
    def _chown_node(self, node: VFSNode, owner: str, group: Optional[str], recursive: bool):
        """Вспомогательная функция для изменения владельца узла"""
        node.owner = owner
        if group:
            node.group = group
        node.modified = datetime.now()
        
        if recursive and node.is_dir:
            for child in node.children.values():
                self._chown_node(child, owner, group, recursive)
    
    def remove(self, path: str, recursive: bool = False, force: bool = False) -> bool:
        """
        Удаляет файл или директорию
        
        Args:
            path: Путь к файлу/директории
            recursive: Рекурсивное удаление директорий
            force: Принудительное удаление без запросов
            
        Returns:
            bool: True если успешно
        """
        node = self.resolve_path(path)
        
        if node is None:
            if not force:
                print(f"rm: невозможно удалить '{path}': Нет такого файла или каталога")
            return False
        
        if node == self.root:
            print(f"rm: невозможно удалить '/': это корневая директория")
            return False
        
        if node.is_dir and not recursive:
            print(f"rm: невозможно удалить '{path}': это каталог")
            print(f"rm: используйте -r для рекурсивного удаления")
            return False
        
        if node.parent is None:
            print(f"rm: невозможно удалить '{path}': нет родительской директории")
            return False
        
        # Если удаляем текущую директорию или её родителя, переходим в корень
        temp = self.current_dir
        while temp is not None:
            if temp == node:
                self.current_dir = self.root
                break
            temp = temp.parent
        
        # Удаляем узел из родительской директории
        del node.parent.children[node.name]
        return True
    
    def get_stats(self) -> Dict[str, int]:
        """Получает статистику VFS"""
        stats = {"files": 0, "directories": 0, "total_size": 0}
        
        def count(node: VFSNode):
            if node.is_dir:
                stats["directories"] += 1
                for child in node.children.values():
                    count(child)
            else:
                stats["files"] += 1
                stats["total_size"] += len(node.content)
        
        count(self.root)
        return stats