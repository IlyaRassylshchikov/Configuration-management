#!/bin/bash
# Полный тест всех команд VFS
# Автор: IlyaRassylshchikov
# Дата: 2025-01-18

# ===== ТЕСТ КОМАНДЫ PWD =====
pwd

# ===== ТЕСТ КОМАНДЫ LS =====
# Простой ls
ls

# ls с длинным форматом
ls -l

# ls конкретной директории
ls home

# ===== ТЕСТ КОМАНДЫ CD =====
# Переход в директорию
cd home
pwd
ls

# Переход в поддиректорию
cd user
pwd
ls

# Переход в documents
cd documents
pwd
ls

# Переход на уровень вверх
cd ..
pwd

# Переход в корень
cd /
pwd

# Абсолютный путь
cd /etc
pwd
ls

# ===== ТЕСТ КОМАНДЫ CAT =====
cd /
cat README.md

cd /etc
cat config.json

cd /home/user/documents
cat report.txt

# ===== ТЕСТ КОМАНДЫ TREE =====
cd /
tree

cd /home
tree

# ===== ТЕСТ КОМАНДЫ FIND =====
cd /
find README.md
find *.txt
find config.json

# ===== ТЕСТ КОМАНДЫ VFS-INFO =====
vfs-info

# ===== ТЕСТ ОБРАБОТКИ ОШИБОК =====
# Несуществующая директория
cd /nonexistent

# Несуществующий файл
cat nonexistent.txt

# cd в файл
cd /README.md

# find несуществующего
find nonexistent_pattern_12345