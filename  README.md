# LMS Platform — Django REST API

[![Django](https://img.shields.io/badge/Django-4.2-green)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-blue)](https://www.django-rest-framework.org/)
[![Docker](https://img.shields.io/badge/Docker-✓-blue)](https://www.docker.com/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-orange)](https://github.com/features/actions)

Система управления обучением (LMS) на базе Django REST Framework, с поддержкой асинхронных задач через Celery, хранением данных в PostgreSQL, кэшированием и брокером сообщений через Redis, и контейнеризацией через Docker.

---

## Production Server

Демо-версия РАБОТАЕТ по адресу: http://89.169.172.245

Доступные endpoints:
- API Root: http://89.169.172.245/api/
- Admin Panel: http://89.169.172.245/admin/
- Swagger Docs: http://89.169.172.245/swagger/
- Redoc Docs: http://89.169.172.245/redoc/

> Примечание: Виртуальная машина включена для проверки. Для экономии средств может быть временно выключена.

---

## Быстрый запуск (локально)

### Предварительные требования
- Docker 20.10+
- Docker Compose v2+
- Python 3.12 (для локальной разработки)

### 1. Клонирование репозитория
```bash
git clone https://github.com/AnnaVal-na/Viewsets-and-Generics.git
cd Viewsets-and-Generics

# Копируем пример env файла
cp .env.example .env

# Редактируем .env файл
nano .env  # или используйте любой текстовый редактор

# Database
DB_NAME=lms_db
DB_USER=postgres
DB_PASSWORD=secure_password_123
DB_HOST=db
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Redis
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

### Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Сборка и запуск контейнеров
docker-compose up --build -d

# Просмотр логов
docker-compose logs -f

# Проверка статуса контейнеров
docker-compose ps


# Применение миграций
docker-compose exec web python manage.py migrate

# Сбор статических файлов
docker-compose exec web python manage.py collectstatic --noinput

# Создание суперпользователя (опционально)
docker-compose exec web python manage.py createsuperuser

### Доступ к приложению
- Приложение: http://localhost
- API: http://localhost/api/
- Admin: http://localhost/admin/
- Документация: http://localhost/swagger/

Локальная разработка (без Docker)

Установка зависимостей
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Настройка базы данных
```bash
# Создание БД PostgreSQL
createdb lms_db

# Или используйте SQLite (измените DATABASES в settings.py)
```

Запуск сервера
```bash
python manage.py migrate
python manage.py runserver
```

Развертывание на сервере (Yandex Cloud)

1. Подготовка сервера
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

2. Настройка проекта на сервере
```bash
# Клонирование проекта
git clone https://github.com/AnnaVal-na/Viewsets-and-Generics.git
cd Viewsets-and-Generics

# Создание .env файла
nano .env  # заполнить настройки для продакшена

# Установка прав (если размещаете в /var/www)
sudo chown -R $USER:$USER /var/www/myapp
chmod -R 755 /var/www/myapp

3. Запуск в продакшн режиме
- Остановка старых контейнеров: docker-compose down
- Запуск новых контейнеров: docker-compose up -d --build
- Проверка статуса: docker-compose ps

CI/CD Pipeline
- Проект использует GitHub Actions для автоматизации
- Workflow файл: .github/workflows/ci-cd.yml
- Этапы pipeline:
  - Lint — проверка кода (flake8, black)
  - Test — запуск тестов с PostgreSQL
  - Build — сборка Docker образов
  - Deploy — автоматический деплой на сервер
- Триггеры:
  - push в ветки: main, develop, final_assignment_fixed
  - pull_request в: main, develop
- Настройка секретов в GitHub:
  - SERVER_IP — IP адрес сервера
  - SSH_USER — пользователь для SSH
  - SSH_PRIVATE_KEY — приватный ключ для доступа

API Endpoints
- Аутентификация
  - POST /api/register/ — регистрация пользователя
  - POST /api/token/ — получение JWT токена
- Пользователи
  - GET /api/users/ — список пользователей (требует аутентификации)
  - GET /api/users/{id}/ — детали пользователя
  - PATCH /api/users/{id}/update/ — обновление пользователя
  - DELETE /api/users/{id}/delete/ — удаление пользователя
- Платежи
  - GET /api/payments/ — список платежей
  - POST /api/payments/ — создание платежа
  - POST /api/payment/create/ — создание платежа через Stripe
  - GET /api/payment/{payment_id}/status/ — проверка статуса платежа
- Курсы и уроки
  - GET /api/courses/ — список курсов
  - GET /api/lessons/ — список уроков

## Тестирование
- Запуск всех тестов: docker-compose exec web python manage.py test
- Запуск с покрытием:
  - docker-compose exec web coverage run manage.py test
  - docker-compose exec web coverage report

4. Запуск конкретного приложения
- docker-compose exec web python manage.py test users
- docker-compose exec web python manage.py test courses

## Безопасность
- JWT аутентификация
- CORS настройки
- Environment variables для чувствительных данных
- Хеширование паролей

## Поддержка
При возникновении проблем:
- Проверьте логи: docker-compose logs
- Убедитесь, что все контейнеры запущены: docker-compose ps
- Проверьте настройки .env файла

## Лицензия
MIT License