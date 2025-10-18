# Shell Emulator - Эмулятор командной оболочки UNIX

Эмулятор командной строки UNIX-подобной ОС, реализованный на Python.

**Версия:** 1.0.0 (Все этапы завершены)  
**Автор:** IlyaRassylshchikov  
**Дата:** 2025-10-18

## Описание проекта

Консольное приложение, эмулирующее работу командной оболочки UNIX с виртуальной файловой системой. Все операции выполняются в памяти без модификации реальной файловой системы.

## Возможности

### Этап 1: REPL 
- Консольный интерфейс (CLI)
- Динамическое приглашение `username@hostname:path$`
- Парсер команд с поддержкой кавычек
- Обработка ошибок
- Команды-заглушки: `ls`, `cd`
- Команда выхода: `exit`

### Этап 2: Конфигурация
- Параметры командной строки: `--vfs`, `--startup`, `--debug`
- Поддержка стартовых скриптов с комментариями
- Имитация диалога при выполнении скриптов
- Отладочный вывод конфигурации

### Этап 3: Виртуальная файловая система (VFS)
- Загрузка VFS из ZIP-архива в память
- Поддержка base64 формата
- Все операции выполняются в памяти
- Команды: `pwd`, `tree`, `vfs-info`

### Этап 4: Основные команды
- **ls** - список файлов с опциями `-l`, `-a`
- **cd** - смена директории (поддержка `.`, `..`, абсолютных и относительных путей)
- **pwd** - вывод текущего пути
- **cat** - вывод содержимого файлов
- **find** - поиск файлов по паттернам (`*.txt`, `file*`)

### Этап 5: Дополнительные команды
- **chown** - изменение владельца файлов и директорий
- **chown -R** - рекурсивное изменение владельца
- **rm** - удаление файлов
- **rm -r** - рекурсивное удаление директорий
- **rm -f** - принудительное удаление

## Установка

### Требования
- Python 3.9 или выше
- ОС: Windows, Linux, macOS

### Установка из репозитория

```bash
# Клонирование репозитория
git clone <repository-url>
cd shell-emulator

# Проверка Python
python --version

# Создание VFS архивов
python scripts/create_vfs_archives.py
```

## Использование

### Базовый запуск

```bash
# Без VFS (режим заглушек)
python shell_emulator.py

# С VFS
python shell_emulator.py --vfs tests/vfs_archives/complex_vfs.zip

# Со стартовым скриптом
python shell_emulator.py --vfs tests/vfs_archives/complex_vfs.zip --startup tests/test_scripts/test_stage5_full.sh

# С отладкой
python shell_emulator.py --vfs tests/vfs_archives/complex_vfs.zip --debug
```

### Параметры командной строки

| Параметр | Описание | Пример |
|----------|----------|--------|
| `--vfs PATH` | Путь к ZIP-архиву VFS | `--vfs tests/vfs_archives/complex_vfs.zip` |
| `--vfs-base64 STRING` | VFS в формате base64 | `--vfs-base64 "UEsDBB..."` |
| `--startup SCRIPT` | Стартовый скрипт | `--startup tests/test_scripts/test_basic.sh` |
| `--debug` | Режим отладки | `--debug` |
| `--version` | Показать версию | `--version` |
| `--help` | Показать справку | `--help` |

## Поддерживаемые команды

### Навигация и просмотр

#### `ls [опции] [путь]`
Список файлов и директорий.

**Опции:**
- `-l` - длинный формат (права, владелец, размер, дата)
- `-a` - показать все файлы (включая скрытые)
- `-la` - комбинация опций

**Примеры:**
```bash
ls
ls -l
ls -la
ls /home
ls /home /etc
```

#### `cd [путь]`
Смена текущей директории.

**Примеры:**
```bash
cd                    # переход в корень
cd /home/user         # абсолютный путь
cd documents          # относительный путь
cd ..                 # на уровень вверх
cd ../..              # на два уровня вверх
```

#### `pwd`
Вывод текущего пути.

**Пример:**
```bash
pwd
# Вывод: /home/user/documents
```

#### `cat [файл...]`
Вывод содержимого файлов.

**Примеры:**
```bash
cat file.txt
cat file1.txt file2.txt
cat /etc/config.json
```

#### `tree`
Визуализация структуры директорий в виде дерева.

**Пример:**
```bash
tree
# Вывод:
# /home/user
# ├── documents/
# │   ├── report.txt
# │   └── letter.txt
# └── downloads/
```

#### `find <паттерн>`
Поиск файлов по имени.

**Паттерны:**
- `filename` - точное имя
- `*.txt` - все файлы с расширением .txt
- `report*` - файлы начинающиеся с report
- `*log*` - файлы содержащие log

**Примеры:**
```bash
find README.md
find *.txt
find *log*
```

### Управление файлами

#### `chown [-R] owner[:group] файл`
Изменение владельца файла или директории.

**Опции:**
- `-R` - рекурсивное изменение

**Примеры:**
```bash
chown alice file.txt                    # изменить владельца
chown bob:developers config.json        # изменить владельца и группу
chown -R admin:staff /home/user         # рекурсивно
```

#### `rm [-rf] файл...`
Удаление файлов и директорий.

**Опции:**
- `-r` или `-R` - рекурсивное удаление директорий
- `-f` - принудительное удаление (без ошибок)

**Примеры:**
```bash
rm file.txt                    # удалить файл
rm file1.txt file2.txt         # удалить несколько файлов
rm -r directory                # удалить директорию
rm -rf /tmp                    # удалить директорию принудительно
```

### Информация и выход

#### `vfs-info`
Информация о виртуальной файловой системе.

**Пример:**
```bash
vfs-info
# Вывод:
# Информация о виртуальной файловой системе:
#   Источник: tests/vfs_archives/complex_vfs.zip
#   Файлов: 16
#   Директорий: 11
#   Общий размер: 892 байт (0.87 КБ)
#   Текущая директория: /
```

#### `exit`
Выход из эмулятора.

## Стартовые скрипты

Скрипты позволяют автоматизировать выполнение команд.

### Синтаксис

```bash
# Комментарий - игнорируется
ls -la
cd /home
cat file.txt

# Кавычки для аргументов с пробелами
ls "my documents"
chown "user name:group name" file.txt
```

### Пример скрипта

```bash
# test_example.sh
# Демонстрация основных команд

# Просмотр корневой директории
ls -l

# Навигация
cd /home/user
pwd

# Просмотр файла
cat documents/report.txt

# Поиск
find *.txt

# Изменение владельца
chown alice documents/report.txt
ls -l documents

# Удаление
rm -r downloads

# Выход
exit
```

### Запуск скрипта

```bash
python shell_emulator.py --vfs tests/vfs_archives/complex_vfs.zip --startup test_example.sh
```

## Структура проекта

```
shell-emulator/
├── shell_emulator.py          # Основной модуль эмулятора
├── config.py                  # Модуль конфигурации
├── vfs.py                     # Виртуальная файловая система
├── README.md                  # Документация
├── requirements.txt           # Зависимости Python
├── tests/
│   ├── test_shell.py         # Автоматические тесты
│   └── test_scripts/         # Тестовые скрипты
│       ├── test_basic.sh
│       ├── test_quotes.sh
│       ├── test_errors.sh
│       ├── test_vfs_full.sh
│       ├── test_stage4_full.sh
│       └── test_stage5_full.sh
├── tests/vfs_archives/        # VFS архивы
│   ├── minimal_vfs.zip
│   ├── medium_vfs.zip
│   └── complex_vfs.zip
└── scripts/                   # Вспомогательные скрипты
    ├── create_vfs_archives.py
    ├── run_stage5_tests.bat
    └── run_stage5_tests.sh
```

## Архитектура

### Основные компоненты

#### 1. ShellEmulator (shell_emulator.py)
Главный класс эмулятора.

**Ключевые методы:**
- `run()` - главный цикл REPL
- `parse_command()` - парсинг команд с использованием `shlex`
- `execute_command()` - диспетчеризация команд
- `execute_script()` - выполнение стартовых скриптов

#### 2. Config (config.py)
Управление конфигурацией.

**Функции:**
- `parse_arguments()` - парсинг аргументов командной строки (argparse)
- `validate_config()` - валидация конфигурации

#### 3. VirtualFileSystem (vfs.py)
Виртуальная файловая система в памяти.

**Структура данных:**
```python
VFSNode:
    - name: str               # Имя файла/директории
    - is_dir: bool           # Флаг директории
    - content: bytes         # Содержимое файла
    - parent: VFSNode        # Родительская директория
    - children: Dict         # Дочерние элементы
    - owner: str             # Владелец
    - group: str             # Группа
```

**Ключевые методы:**
- `load_from_zip()` - загрузка VFS из ZIP
- `resolve_path()` - разрешение путей
- `change_directory()` - смена директории
- `list_directory()` - список содержимого
- `cat()` - чтение файла
- `find()` - поиск файлов
- `chown()` - изменение владельца
- `remove()` - удаление файлов/директорий

### Ключевые технические решения

#### Парсинг команд с кавычками
```python
import shlex

def parse_command(self, input_line: str):
    # shlex.split автоматически обрабатывает кавычки
    tokens = shlex.split(input_line)
    # "my file.txt" → my file.txt (без кавычек)
    
    command = tokens[0]
    args = tokens[1:]
    return command, args
```

#### Древовидная структура VFS
```python
class VFSNode:
    def __init__(self, name, is_dir=False, content=b""):
        self.name = name
        self.is_dir = is_dir
        self.content = content       # Хранится в памяти
        self.children = {}           # Словарь дочерних узлов
        self.parent = None

# Пример структуры в памяти:
# root (/)
# ├── home (VFSNode, is_dir=True)
# │   └── user (VFSNode, is_dir=True)
# │       └── file.txt (VFSNode, content=b"text")
# └── etc (VFSNode, is_dir=True)
```

#### Разрешение путей
```python
def resolve_path(self, path: str) -> Optional[VFSNode]:
    # Обработка специальных путей
    if path == '.':
        return self.current_dir
    if path == '..':
        return self.current_dir.parent or self.current_dir
    
    # Абсолютный или относительный путь
    if path.startswith('/'):
        current = self.root
        path = path[1:]
    else:
        current = self.current_dir
    
    # Проход по частям пути
    for part in path.split('/'):
        if part == '..':
            current = current.parent or current
        elif part not in ('.', ''):
            current = current.children.get(part)
            if current is None:
                return None
    
    return current
```

## Тестирование

### Автоматические тесты

```bash
# Python тесты
python tests/test_shell.py
```

### Интеграционные тесты

```bash
# Windows
scripts\run_stage5_tests.bat

# Linux/macOS
bash scripts/run_stage5_tests.sh
```

### Ручное тестирование

#### Сценарий 1: Базовые команды
```bash
python shell_emulator.py --vfs tests/vfs_archives/complex_vfs.zip

# В эмуляторе:
ls
ls -l
cd home/user
pwd
cat documents/report.txt
tree
exit
```

#### Сценарий 2: Управление файлами
```bash
python shell_emulator.py --vfs tests/vfs_archives/complex_vfs.zip

# В эмуляторе:
ls -l
chown alice README.md
ls -l README.md
cd /tmp
rm temp1.txt
ls
cd /
rm -r tmp
ls
exit
```

#### Сценарий 3: Поиск и навигация
```bash
python shell_emulator.py --vfs tests/vfs_archives/complex_vfs.zip

# В эмуляторе:
find *.txt
find *log*
cd /var/log
cat system.log
cd /
tree
exit
```

## Создание VFS архивов

### Автоматическое создание

```bash
python scripts/create_vfs_archives.py
```

Создаст три тестовых архива:
- `minimal_vfs.zip` - минимальный (1 файл)
- `medium_vfs.zip` - средний (несколько файлов, 2 уровня)
- `complex_vfs.zip` - сложный (3+ уровня, разные типы файлов)

### Создание собственного VFS

```python
import zipfile

with zipfile.ZipFile('my_vfs.zip', 'w') as zf:
    # Добавление файлов
    zf.writestr('file.txt', 'Content')
    zf.writestr('dir/subfile.txt', 'More content')
    
    # Добавление пустых директорий
    zf.writestr('empty_dir/', '')

# Использование
python shell_emulator.py --vfs my_vfs.zip
```

## Обработка ошибок

### Команды не найдены
```bash
user@host:/$ unknown_command
Ошибка: команда не найдена: unknown_command
```

### Несуществующие файлы/директории
```bash
user@host:/$ cd /nonexistent
cd: /nonexistent: Нет такого файла или каталога

user@host:/$ cat fake.txt
cat: fake.txt: Нет такого файла или каталога
```

### Некорректные операции
```bash
user@host:/$ cd /README.md
cd: /README.md: Не является каталогом

user@host:/$ rm /etc
rm: невозможно удалить '/etc': это каталог
rm: используйте -r для рекурсивного удаления

user@host:/$ rm -rf /
rm: невозможно удалить '/': это корневая директория
```

## Особенности реализации

### Безопасность
- Защита корневой директории от удаления
- Автоматический переход в корень при удалении текущей директории
- Валидация всех путей перед операциями

### Производительность
- Все операции в памяти (O(1) для большинства операций)
- Эффективный поиск через словари Python
- Ленивая загрузка содержимого файлов

### Кросс-платформенность
- Работает на Windows, Linux, macOS
- Использование `PurePosixPath` для путей VFS
- Универсальные тестовые скрипты (.sh и .bat)

## Ограничения

- VFS загружается полностью в память (ограничение по размеру)
- Нет поддержки символических ссылок
- Права доступа эмулируются (не проверяются реально)
- Нет поддержки конкуррентного доступа

## Часто задаваемые вопросы (FAQ)

### Как изменить приглашение?
Отредактируйте метод `get_prompt()` в `shell_emulator.py`:
```python
def get_prompt(self) -> str:
    return "$ "  # Упрощенное приглашение
```

### Как добавить новую команду?
1. Добавьте метод в класс `ShellEmulator`:
```python
def cmd_mycommand(self, args: List[str]) -> None:
    print(f"My command with args: {args}")
```

2. Зарегистрируйте команду в `__init__`:
```python
self.commands = {
    # ...
    'mycommand': self.cmd_mycommand,
}
```

### Как работать с бинарными файлами?
Команда `cat` автоматически определяет бинарные файлы и выводит их в base64:
```bash
cat binary_file.jpg
# Вывод: [Бинарный файл, base64]:
# /9j/4AAQSkZJRgABAQEAYABgAAD...
```

### Можно ли сохранить изменения VFS?
Нет, все изменения существуют только в памяти. После выхода из эмулятора они теряются. Это сделано по требованиям задания.

## Примеры использования

### Пример 1: Просмотр структуры проекта
```bash
python shell_emulator.py --vfs tests/vfs_archives/complex_vfs.zip <<EOF
tree
vfs-info
exit
EOF
```

### Пример 2: Поиск всех конфигурационных файлов
```bash
python shell_emulator.py --vfs tests/vfs_archives/complex_vfs.zip <<EOF
find *.json
find *.conf
find *config*
exit
EOF
```

### Пример 3: Изменение владельцев всех файлов проекта
```bash
python shell_emulator.py --vfs tests/vfs_archives/complex_vfs.zip <<EOF
chown -R admin:staff /home
ls -l /home
ls -l /home/user
ls -l /home/user/documents
exit
EOF
```

## Разработка и отладка

### Режим отладки
```bash
python shell_emulator.py --vfs tests/vfs_archives/complex_vfs.zip --debug
```

