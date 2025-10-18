#!/bin/bash
# Тестовый скрипт: работа с кавычками
# Проверяет корректность обработки аргументов в кавычках

# Комментарий: двойные кавычки
ls "file with spaces.txt"
cd "My Documents"

# Комментарий: одинарные кавычки
ls 'another file.doc'
cd 'Program Files'

# Комментарий: смешанные аргументы
ls "file 1" 'file 2' file3 -la

# Комментарий: сложные пути с пробелами
cd "/home/user/My Documents/Work Files"
ls -l "/usr/local/Program Files" '/opt/my software'