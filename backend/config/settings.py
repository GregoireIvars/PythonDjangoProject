# filepath: c:\Users\frus84312\AppPython\backend\config\settings.py
"""
Django settings for config project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Configuration des fichiers média
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-change-me')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # ✅ Middleware pour la langue
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # ✅ Doit être présent
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'blog.middleware.NoCacheMiddleware',  # Votre middleware personnalisé
]

ROOT_URLCONF = 'config.urls'

# Paramètres CSRF
CSRF_COOKIE_SECURE = False  # True en production avec HTTPS
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SAMESITE = 'Lax'

# En développement
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.timestamp_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'postgresSQL_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

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

# ===================================
# INTERNATIONALISATION ET TRADUCTION
# ===================================

LANGUAGE_CODE = 'fr'  # Langue par défaut
TIME_ZONE = 'Europe/Paris'

# ===================================
# CONFIGURATION DE L'API OpenAI
# ===================================
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("La clé API OpenAI est requise. Veuillez la définir dans le fichier .env ou comme variable d'environnement.")

USE_I18N = True  # Active l'internationalisation
USE_L10N = True  # Active la localisation
USE_TZ = True

# Langues supportées
LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
    ('es', 'Español'),
]

# Chemins vers les fichiers de traduction
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'blog/static'),
]

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

CACHE_MIDDLEWARE_SECONDS = 0
USE_ETAGS = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'blog:home'      # Où aller après connexion réussie
LOGOUT_REDIRECT_URL = 'blog:home'     # Où aller après déconnexion

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# Configuration pour l'environnement de production
# En production, ces variables doivent être définies sur le serveur