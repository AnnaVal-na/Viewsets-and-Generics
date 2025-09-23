# Educational Platform API

Django REST Framework API для образовательной платформы с курсами, уроками и системой платежей.

## Описание

RESTful API для управления образовательным контентом с расширенной системой прав доступа, 
JWT-авторизацией, системой подписок, интеграцией с Stripe и возможностью фильтрации и сортировки данных.

## Основные функции

-  JWT-авторизация — безопасный доступ к API
-  Ролевая модель — пользователи, модераторы, администраторы
-  Права доступа — владельцы могут управлять только своим контентом
-  CRUD-операции — полный набор для курсов, уроков, пользователей и платежей
-  Фильтрация и сортировка — удобный поиск и упорядочивание данных
-  Платежная система — интеграция с Stripe для оплаты курсов и уроков
-  Система подписок — подписка на обновления курсов
-  Валидация контента — проверка YouTube-ссылок в материалах
-  Пагинация — постраничный вывод данных
-  Документация API — автоматическая генерация Swagger/Redoc

##  Установка и запуск

### 1. Клонирование репозитория
```
git clone <URL вашего репозитория>
cd Viewsets-and-Generics
```

### 2. Создание виртуального окружения
- Linux/macOS:
```
python -m venv venv
source venv/bin/activate
```
- Windows ( CMD ):
```
python -m venv venv
venv\Scripts\activate.bat
```
- Windows ( PowerShell ):
```
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Установка зависимостей
```
pip install -r requirements.txt
```

### 4. Настройка базы данных
Создайте файл .env в корне проекта и заполните необходимые параметры:

```dotenv
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_secret_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
```

### 5. Применение миграций
```
python manage.py makemigrations
python manage.py migrate
```

### 6. Создание суперпользователя
```
python manage.py createsuperuser
```

### 7. Запуск сервера
```
python manage.py runserver
```

## API Endpoints

Аутентификация
```
POST /api/token/           - Получение JWT токена
POST /api/token/refresh/    - Обновление токена
POST /api/register/         - Регистрация нового пользователя
```

Пользователи
```
GET  /api/users/                 - Список пользователей (требует авторизации)
GET  /api/users/{id}/             - Детали пользователя
PUT  /api/users/{id}/update/      - Обновление пользователя
DELETE /api/users/{id}/delete/    - Удаление пользователя
```

Курсы
```
GET  /api/courses/              - Список курсов с пагинацией
POST /api/courses/              - Создание курса (требует авторизации)
GET  /api/courses/{id}/          - Детали курса с информацией о подписке
PUT  /api/courses/{id}/          - Обновление курса
DELETE /api/courses/{id}/        - Удаление курса
```

Уроки
```
GET  /api/lessons/              - Список уроков с пагинацией
POST /api/lessons/              - Создание урока (требуется авторизация, валидация YouTube-ссылок)
GET  /api/lessons/{id}/          - Детали урока
PUT  /api/lessons/{id}/          - Обновление урока
DELETE /api/lessons/{id}/        - Удаление урока
```

Подписки
```
POST /api/subscribe/             - Управление подпиской на курс
```

Платежи
```
GET  /api/payments/              - Список платежей (требует авторизации)
POST /api/payment/create/        - Создание платежной сессии Stripe
GET  /api/payment/{payment_id}/status/ - Проверка статуса платежа
```

Документация
```
GET /swagger/                   - Интерактивная документация Swagger
GET /redoc/                     - Документация Redoc
```
Структура проекта:
- courses/
- models.py: Course, Lesson, Subscription
- serializers.py: валидация и преобразование данных
- views.py: ViewSets/APIViews
- validators.py: валидатор YouTube-ссылок (если нужен)
- paginators.py: настройки пагинации
- tests.py: тесты
- users/
- models.py: CustomUser, Payment
- views.py: ViewSets
- services.py: сервисы Stripe
- permissions.py: кастомные permissions
- myproject/: настройки проекта
- requirements.txt: зависимости

## Запуск через Docker Compose

### 1. Клонирование и настройка
```bash
git clone <your-repo-url>
cd Viewsets-and-Generics
cp .env.example .env

## Проверка работоспособности:

1. Django: http://localhost:8000
2. База данных: 
   ```bash
   docker-compose exec db psql -U postgres -d viewsets_generics_db

Redis:
bash
docker-compose exec redis redis-cli ping
Celery:

bash
docker-compose logs celery
text

## Деплой на продакшен сервер

### Требования к серверу:
- Ubuntu 20.04+
- Python 3.9+
- PostgreSQL
- Redis
- Nginx
- Gunicorn

### Настройка сервера:

1. Подключитесь к серверу по SSH
2. Выполните команды настройки:
```bash
# Установите необходимые пакеты
sudo apt update && sudo apt install -y python3-pip python3-venv nginx postgresql redis-server

# Настройте базу данных
sudo -u postgres psql
CREATE DATABASE myapp_db;
CREATE USER myapp_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE myapp_db TO myapp_user;

## Server Setup

1. Install dependencies:
```bash
sudo apt update
sudo apt install nginx postgresql python3-pip
