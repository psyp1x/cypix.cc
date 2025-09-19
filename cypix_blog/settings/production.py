import os
from pathlib import Path
import dj_database_url
from .base import MIDDLEWARE

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = [
    'cypix.cc',
    '*.railway.app',
    'localhost',
    '127.0.0.1',
]

# Database

# Prefer a single DATABASE_URL if provided by Railway; otherwise fall back to
# individual PG*/POSTGRES_* environment variables.
_database_url = os.environ.get('DATABASE_URL')
if _database_url:
    DATABASES = {
        'default': dj_database_url.parse(_database_url, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('PGDATABASE') or os.environ.get('POSTGRES_DB', 'railway'),
            'USER': os.environ.get('PGUSER') or os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('PGPASSWORD') or os.environ.get('POSTGRES_PASSWORD', ''),
            'HOST': os.environ.get('PGHOST') or os.environ.get('POSTGRES_HOST', 'postgres.railway.internal'),
            'PORT': os.environ.get('PGPORT') or os.environ.get('POSTGRES_PORT', '5432'),
        }
    }

# Static files configuration
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Ensure CSRF works for deployed domains
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://cypix.cc',
]

# Add whitenoise middleware
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
