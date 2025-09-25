# Многостадийный Dockerfile для Django приложения
FROM python:3.12-slim as builder

# Устанавливаем зависимости системы для сборки
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.12-slim

# Устанавливаем системные зависимости для runtime
RUN apt-get update && apt-get install -y \
    libpq5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя для безопасности
RUN useradd --create-home --shell /bin/bash app
WORKDIR /home/app

# Копируем установленные зависимости из стадии builder
COPY --from=builder /root/.local /home/app/.local
COPY --chown=app:app . .

# Настраиваем пути
ENV PATH=/home/app/.local/bin:$PATH
ENV PYTHONPATH=/home/app

# Создаем директории для статики и медиа
RUN mkdir -p /home/app/staticfiles /home/app/media
RUN chown -R app:app /home/app/

# Переключаемся на пользователя app
USER app

# Открываем порт
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/', timeout=10)"

# Команда запуска
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "myproject.wsgi:application"]

