FROM python:3.13-slim

WORKDIR /app

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей
COPY pyproject.toml poetry.lock* ./

# Установка Poetry
RUN pip install poetry

# Установка зависимостей проекта без установки текущего проекта
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Копирование проекта
COPY . .

# Создание необходимых директорий
RUN mkdir -p logs staticfiles

# Применение миграций и сборка статических файлов
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]