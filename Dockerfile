# Используем официальный Python образ как базовый
FROM python:3.12-slim as base

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /src

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry
RUN pip install poetry

# Настраиваем Poetry для работы в контейнере
RUN poetry config virtualenvs.create false

# Устанавливаем зависимости
RUN poetry install

# Копируем исходный код
COPY src/ ./src/
COPY config.yml ./
COPY alembic.ini ./
COPY alembic/ ./alembic/

# Создаем пользователя для безопасности
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /src
USER appuser

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
