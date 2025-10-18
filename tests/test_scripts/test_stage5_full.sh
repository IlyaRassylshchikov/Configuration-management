#!/bin/bash
# Полный тестовый скрипт для Этапа 5
# Автор: IlyaRassylshchikov
# Дата: 2025-10-18

# ===== НАЧАЛЬНОЕ СОСТОЯНИЕ =====

pwd
ls -l

# ===== ТЕСТ КОМАНДЫ CHOWN =====

# Просмотр текущих владельцев
cd /
ls -l

# Изменение владельца одного файла
chown alice README.md
ls -l README.md

# Изменение владельца и группы
chown bob:developers etc/config.json
ls -l etc/config.json

# Изменение владельца директории (не рекурсивно)
chown charlie home
ls -l home

# Рекурсивное изменение владельца
chown -R dave:admins home/user
ls -l home
ls -l home/user
ls -l home/user/documents

# Изменение владельца несуществующего файла (ошибка)
chown alice nonexistent.txt

# ===== ТЕСТ КОМАНДЫ RM =====

# Удаление одного файла
cd /tmp
ls
rm temp1.txt
ls

# Попытка удалить директорию без -r (ошибка)
cd /
rm tmp

# Удаление директории с -r
rm -r tmp
ls

# Проверка что директория удалена
ls tmp

# Создание тестового случая для удаления
cd /home/user
ls

# Удаление файла
rm documents/letter.txt
ls documents

# Удаление директории с содержимым
rm -r documents
ls

# Удаление несуществующего файла (ошибка без -f)
rm nonexistent.txt

# Удаление несуществующего файла с -f (без ошибки)
rm -f nonexistent.txt

# Попытка удалить корневую директорию (ошибка)
rm -rf /

# ===== КОМБИНИРОВАННЫЕ ТЕСТЫ =====

# Изменение владельца и затем удаление
cd /etc
ls -l
chown testuser hosts
ls -l hosts
rm hosts
ls

# Рекурсивная смена владельца и удаление директории
cd /
chown -R admin:sysadmin var
ls -l var
rm -r var/log
ls var

# ===== ПРОВЕРКА СОСТОЯНИЯ ПОСЛЕ ИЗМЕНЕНИЙ =====

cd /
tree
vfs-info
ls -l

# ===== ТЕСТ ОБРАБОТКИ ОШИБОК =====

# chown с неверным форматом
chown
chown owner

# rm без аргументов
rm

# chown несуществующего файла
chown user /path/to/nowhere

# rm несуществующего файла
rm /path/to/nowhere

exit