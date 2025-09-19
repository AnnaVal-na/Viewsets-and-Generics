from myproject.settings import *

# Используем SQLite для тестов
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# ОТКЛЮЧАЕМ SSL и HTTPS для тестов
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_PROXY_SSL_HEADER = None

# Отключаем редиректы
APPEND_SLASH = False

# Отключаем кэширование для тестов
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Создаем папку static
import os
os.makedirs('static', exist_ok=True)
