#!/bin/bash

echo "--- Настройка Telegram YouTube Bot ---"
read -p "Введите Bot Token: " BOT_TOKEN
read -p "Введите API ID: " API_ID
read -p "Введите API Hash: " API_HASH
read -p "Введите ID канала (например, -100...): " CHANNEL_ID
read -p "Введите ссылку на канал (https://t.me/...): " CHANNEL_LINK
read -p "Введите ID админа (ваш ID): " ADMIN_ID

cat <<EOF > .env
BOT_TOKEN=$BOT_TOKEN
API_ID=$API_ID
API_HASH=$API_HASH
CHANNEL_ID=$CHANNEL_ID
CHANNEL_LINK=$CHANNEL_LINK
ADMIN_ID=$ADMIN_ID
EOF

echo "Файл .env успешно создан!"
