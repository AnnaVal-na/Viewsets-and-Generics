# LMS Platform - Django REST API

Система управления обучением (LMS) с использованием Django REST Framework, Celery, Redis, PostgreSQL и Docker.

## Production Server

**Демо-версия доступна по адресу:** http://89.169.172.245

---

## Быстрый запуск (локально)

### Требования
- Docker 20.10+
- Docker Compose v2+

### Запуск
```bash
git clone https://github.com/AnnaVal-na/Viewsets-and-Generics.git
cd Viewsets-and-Generics
cp .env.example .env  # отредактируйте под себя
docker-compose up --build