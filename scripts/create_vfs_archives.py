#!/usr/bin/env python3
"""
Скрипт для создания тестовых VFS архивов
"""

import zipfile
import base64
from pathlib import Path


def create_minimal_vfs():
    """Создаёт минимальный VFS (1 файл)"""
    print("Создание minimal_vfs.zip...")
    
    zip_path = Path("tests/vfs_archives/minimal_vfs.zip")
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("readme.txt", "Это минимальная виртуальная файловая система.\nОдин файл в корне.\n")
    
    print(f"  ✓ Создан: {zip_path}")
    print(f"    Размер: {zip_path.stat().st_size} байт")
    return zip_path


def create_medium_vfs():
    """Создаёт средний VFS (несколько файлов и 1 уровень директорий)"""
    print("\nСоздание medium_vfs.zip...")
    
    zip_path = Path("tests/vfs_archives/medium_vfs.zip")
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Корневые файлы
        zf.writestr("readme.txt", "Средняя виртуальная файловая система\n")
        zf.writestr("hello.py", "#!/usr/bin/env python3\nprint('Hello from VFS!')\n")
        zf.writestr("notes.txt", "Заметки:\n1. Проверить VFS\n2. Протестировать команды\n")
        
        # Директория docs
        zf.writestr("docs/", "")
        zf.writestr("docs/manual.txt", "Руководство пользователя\n\nКоманды:\n- ls\n- cd\n- pwd\n")
        zf.writestr("docs/faq.txt", "Часто задаваемые вопросы\n\nQ: Как выйти?\nA: Введите exit\n")
        
        # Директория src
        zf.writestr("src/", "")
        zf.writestr("src/main.py", "def main():\n    print('Main function')\n")
        zf.writestr("src/utils.py", "def helper():\n    return 'Helper'\n")
    
    print(f"  ✓ Создан: {zip_path}")
    print(f"    Размер: {zip_path.stat().st_size} байт")
    return zip_path


def create_complex_vfs():
    """Создаёт сложный VFS (3+ уровня директорий, разные типы файлов)"""
    print("\nСоздание complex_vfs.zip...")
    
    zip_path = Path("tests/vfs_archives/complex_vfs.zip")
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Корень
        zf.writestr("README.md", "# Сложная VFS\n\nМного файлов и глубокая структура директорий.\n")
        zf.writestr(".gitignore", "*.pyc\n__pycache__/\n*.log\n")
        
        # /home
        zf.writestr("home/", "")
        zf.writestr("home/user/", "")
        zf.writestr("home/user/documents/", "")
        zf.writestr("home/user/documents/report.txt", "Отчёт за 2025 год\n\nВсе показатели в норме.\n")
        zf.writestr("home/user/documents/letter.txt", "Уважаемый коллега,\n\nПишу вам по поводу...\n")
        
        zf.writestr("home/user/downloads/", "")
        zf.writestr("home/user/downloads/file1.zip", b"PK\x03\x04fake")
        zf.writestr("home/user/downloads/image.jpg", b"\xff\xd8\xff\xe0fake_jpeg")
        
        # /etc
        zf.writestr("etc/", "")
        zf.writestr("etc/config.json", '{\n  "version": "1.0",\n  "debug": false\n}\n')
        zf.writestr("etc/hosts", "127.0.0.1 localhost\n::1 localhost\n")
        
        # /var
        zf.writestr("var/", "")
        zf.writestr("var/log/", "")
        zf.writestr("var/log/system.log", "[2025-01-18 10:00:00] System started\n[2025-01-18 10:01:00] All services OK\n")
        zf.writestr("var/log/error.log", "[2025-01-18 10:05:00] Warning: Low disk space\n")
        
        # /usr
        zf.writestr("usr/", "")
        zf.writestr("usr/bin/", "")
        zf.writestr("usr/bin/script.sh", "#!/bin/bash\necho 'Hello from script'\n")
        
        zf.writestr("usr/share/", "")
        zf.writestr("usr/share/data/", "")
        zf.writestr("usr/share/data/database.txt", "id,name,value\n1,test,100\n2,prod,200\n")
        
        # /tmp
        zf.writestr("tmp/", "")
        zf.writestr("tmp/temp1.txt", "Временный файл 1\n")
        zf.writestr("tmp/temp2.txt", "Временный файл 2\n")
    
    print(f"  ✓ Создан: {zip_path}")
    print(f"    Размер: {zip_path.stat().st_size} байт")
    return zip_path


def create_base64_example(zip_path: Path):
    """Создаёт base64 версию архива для примера"""
    print(f"\nСоздание base64 версии {zip_path.name}...")
    
    with open(zip_path, 'rb') as f:
        zip_data = f.read()
    
    b64_data = base64.b64encode(zip_data).decode('ascii')
    
    output_path = zip_path.with_suffix('.base64.txt')
    with open(output_path, 'w') as f:
        f.write(b64_data)
    
    print(f"  ✓ Создан: {output_path}")
    print(f"    Размер: {output_path.stat().st_size} байт")
    print(f"    Первые 50 символов: {b64_data[:50]}...")
    return output_path


def main():
    """Создаёт все тестовые VFS архивы"""
    print("="*60)
    print("Создание тестовых VFS архивов")
    print("="*60)
    
    minimal = create_minimal_vfs()
    medium = create_medium_vfs()
    complex_vfs = create_complex_vfs()
    
    print("\n" + "="*60)
    print("Создание base64 версий (для тестирования --vfs-base64)")
    print("="*60)
    
    create_base64_example(minimal)
    
    print("\n" + "="*60)
    print("✓ Все VFS архивы созданы успешно!")
    print("="*60)
    print("\nТеперь можно тестировать:")
    print(f"  python shell_emulator.py --vfs {minimal}")
    print(f"  python shell_emulator.py --vfs {medium}")
    print(f"  python shell_emulator.py --vfs {complex_vfs}")


if __name__ == "__main__":
    main()