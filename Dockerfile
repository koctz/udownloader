FROM python:3.10-slim

# Установка системных зависимостей: ffmpeg, curl и Node.js
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Сначала копируем зависимости для кэширования слоев
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Создаем папку для загрузок внутри контейнера
RUN mkdir -p /app/downloads && chmod 777 /app/downloads

CMD ["python", "bot.py"]
