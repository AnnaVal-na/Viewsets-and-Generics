import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Путь к корню проекта (например, папка Viewsets-and-Generics)
BASE_DIR = Path(__file__).resolve().parent.parent

# Безопасность
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-very-secret-key-for-dev-only')  # Установи нормальный ключ в .env!
DEBUG = True  # В продакшене обязательно поставь False

# Разрешённые хосты
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']  # Добавь домены, если нужно

# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Третьесторонние
    'rest_framework',  # Django REST Framework

    # Локальные приложения
    'users',
    'courses',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL-конфигурация
ROOT_URLCONF = 'myproject.urls'  # ← Убедись, что имя проекта правильное (например, myproject)

# Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Можно добавить пути, например [BASE_DIR / 'templates']
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'myproject.wsgi.application'  # ← Проверь имя проекта

# База данных — PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": int(os.getenv("DB_PORT", 5432)),
    }
}

# Валидация паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Локализация
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'  # или 'UTC', как у тебя
USE_I18N = True
USE_TZ = True

# Статические файлы
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Для collectstatic в продакшене
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Локальные статические файлы
]

# Медиа-файлы (аватарки и т.д.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Кастомная модель пользователя
AUTH_USER_MODEL = 'users.CustomUser'

# Настройки Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Email (для разработки — в консоль)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Дефолтный авто-филд
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
