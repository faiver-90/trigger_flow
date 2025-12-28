FROM python:3.12-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Отключаем создание виртуального окружения внутри poetry
RUN poetry config virtualenvs.create false

WORKDIR /app

# Копируем файлы для установки зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry install --no-root --with dev

# Копируем всё остальное
COPY . .
