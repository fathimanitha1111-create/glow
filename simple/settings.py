"""
Django settings for simple project.

Configured for Glow & Care Skincare E-Commerce Website.
Optimized for local development (SQLite) and production deployment on Vercel with Neon PostgreSQL.
"""
import os
import sys
import pathlib
from dotenv import load_dotenv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# Load environment variables from .env file if present
load_dotenv(BASE_DIR / ".env")

is_vercel = os.getenv('VERCEL') == '1'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-simple-glow-skincare-secret-key-2026-xyz')

# SECURITY WARNING: don't run with debug turned on in production!
debug_env = os.getenv('DEBUG')
if debug_env is not None:
    DEBUG = debug_env.lower() in ('true', '1', 'yes')
else:
    # On Vercel production default to False; locally default to True
    DEBUG = False if is_vercel else True

# ALLOWED_HOSTS: Read from environment variable (comma-separated), with safe local & Vercel defaults
allowed_hosts_env = os.getenv('ALLOWED_HOSTS', '')
if allowed_hosts_env:
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',') if host.strip()]
else:
    ALLOWED_HOSTS = ['*']

for host in ['.vercel.app', 'glow-withme.vercel.app', 'localhost', '127.0.0.1', '[::1]', 'testserver']:
    if host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(host)

# CSRF_TRUSTED_ORIGINS: Required for secure HTTPS forms on Vercel and locally
csrf_trusted_env = os.getenv('CSRF_TRUSTED_ORIGINS', '')
if csrf_trusted_env:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_trusted_env.split(',') if origin.strip()]
else:
    CSRF_TRUSTED_ORIGINS = [
        'https://*.vercel.app',
        'https://glow-withme.vercel.app',
        'http://localhost:8000',
        'http://127.0.0.1:8000'
    ]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom simpleapp
    'simpleapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'simple.urls'

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
                'django.template.context_processors.media',
                # Custom cart context processor to show live cart count on all pages
                'simpleapp.context_processors.cart_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'simple.wsgi.application'

# Database Configuration
# Uses PostgreSQL when a valid DATABASE_URL is set (Neon / Supabase / etc.)
# Otherwise uses SQLite (persisted locally; copied to writable /tmp on Vercel serverless)
DATABASE_URL = os.getenv('DATABASE_URL', '').strip()

# Check if DATABASE_URL is valid and not a placeholder template
is_valid_remote_db = (
    bool(DATABASE_URL) and
    'YOUR_PASSWORD' not in DATABASE_URL and
    'ep-xyz' not in DATABASE_URL and
    'ep-solitary-voice' not in DATABASE_URL
)

if is_valid_remote_db:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True if ('neon.tech' in DATABASE_URL or 'sslmode=require' in DATABASE_URL or not DEBUG) else False,
        )
    }
else:
    if is_vercel:
        import shutil
        import tempfile
        tmp_dir = pathlib.Path(tempfile.gettempdir())
        tmp_db = tmp_dir / 'db.sqlite3'
        src_db = BASE_DIR / 'db.sqlite3'
        # Copy pre-populated SQLite database to writable temp directory on cold start
        if not tmp_db.exists() and src_db.exists():
            try:
                shutil.copy2(src_db, tmp_db)
            except Exception:
                pass
        db_path = tmp_db
    else:
        db_path = BASE_DIR / 'db.sqlite3'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': db_path,
        }
    }

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_USE_FINDERS = True

# Media files (Product uploads)
MEDIA_URL = '/media/'
import tempfile
MEDIA_ROOT = (pathlib.Path(tempfile.gettempdir()) / 'media') if is_vercel else (BASE_DIR / 'media')

# Authentication URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
