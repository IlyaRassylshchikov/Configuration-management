#!/bin/bash
# Тестовый скрипт: базовые команды
# Автор: IlyaRassylshchikov
# Дата: 2025-10-17

# Проверка команды ls без аргументов
ls

# Проверка команды ls с аргументами
ls -la
ls -l /home /usr/bin

# Проверка команды cd
cd
cd /home
cd /usr/local/bin

# Проверка сложных путей
cd /etc/systemd/system
ls -lah /var/log