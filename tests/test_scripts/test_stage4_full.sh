#!/bin/bash
# Полный тестовый скрипт для Этапа 4
# Автор: IlyaRassylshchikov
# Дата: 2025-10-18

# ===== ТЕСТ КОМАНДЫ LS =====

# Простой ls
ls

# ls с длинным форматом
ls -l

# ls всех файлов
ls -a

# ls комбинированные опции
ls -la

# ls конкретной директории
ls home

# ls нескольких директорий
ls home etc

# ls несуществующей директории (ошибка)
ls nonexistent

# ===== ТЕСТ КОМАНДЫ CD =====

# Переход в директорию
cd home
pwd

# Переход в поддиректорию
cd user
pwd

# Переход еще глубже
cd documents
pwd

# Вывод содержимого
ls

# Переход на уровень вверх
cd ..
pwd

# Переход на два уровня вверх
cd ../..
pwd

# Абсолютный путь
cd /etc
pwd

# Переход в корень без аргументов
cd
pwd

# Переход по относительному пути
cd home/user/downloads
pwd

# Попытка cd в файл (ошибка)
cd /README.md

# Попытка cd в несуществующую директорию (ошибка)
cd /nonexistent/path

# ===== ТЕСТ КОМАНДЫ PWD =====

cd /
pwd

cd /home/user
pwd

cd documents
pwd

# ===== ТЕСТ КОМАНДЫ CAT =====

cd /

# Вывод одного файла
cat README.md

# Вывод файла из другой директории
cat etc/config.json

# Вывод нескольких файлов
cat README.md etc/hosts

cd /home/user/documents

# Вывод файлов в текущей директории
cat report.txt
cat letter.txt

# Вывод нескольких файлов сразу
cat report.txt letter.txt

# cat несуществующего файла (ошибка)
cat nonexistent.txt

# cat директории (ошибка)
cat /home

# cat без аргументов (ошибка)
cd /

# ===== ТЕСТ КОМАНДЫ FIND =====

# Поиск по точному имени
find README.md

# Поиск с паттерном (все txt файлы)
find *.txt

# Поиск с паттерном (все файлы начинающиеся с report)
find report*

# Поиск с паттерном (все файлы заканчивающиеся на .json)
find *.json

# Поиск с паттерном (все файлы содержащие log)
find *log*

# Поиск всех файлов
find *

# Поиск несуществующего файла
find nonexistent_file_12345.xyz

# ===== КОМБИНИРОВАННЫЕ ТЕСТЫ =====

# Навигация и просмотр файлов
cd /var/log
pwd
ls
cat system.log
cat error.log

# Поиск и просмотр
cd /
find *.log
cat var/log/system.log

# Навигация по сложному пути
cd /usr/share/data
pwd
ls
cat database.txt

# Возврат в корень и проверка
cd /
pwd
tree

# ===== ТЕСТ VFS-INFO =====
vfs-info

# ===== ТЕСТ ОБРАБОТКИ ОШИБОК =====

# Команда с неверными аргументами
cd /home /etc

# Несуществующая команда
unknown_command arg1 arg2

# Завершение
exit