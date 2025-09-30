# Используем многостадийную сборку
FROM python:3.12-slim AS builder

# Устанавливаем зависимости для сборки
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# Финальный образ
FROM python:3.12-slim

# Устанавливаем runtime-зависимости
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя
RUN useradd --create-home --shell /bin/bash app
WORKDIR /home/app

# Копируем зависимости из builder
COPY --from=builder /root/.local /home/app/.local

# Копируем код (без .git, __pycache__ и т.д.)
COPY --chown=app:app . .

# Устанавливаем права
RUN mkdir -p /home/app/staticfiles /home/app/media
RUN chown -R app:app /home/app

# Настраиваем пути
ENV PATH=/home/app/.local/bin:$PATH
ENV PYTHONPATH=/home/app

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "myproject.wsgi:application"]