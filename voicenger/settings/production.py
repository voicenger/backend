# voicenger/settings/production.py

from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': config("ENGINE", "django.db.backends.postgresql_psycopg2"),
        'NAME': config("DB_NAME", default="postgres"),
        'USER': config("DB_USER", default="postgres"),
        'PASSWORD': config("DB_PASSWORD", default="postgres"),
        'HOST': config("DB_HOST", default="postgres"),
        'PORT': config("DB_PORT", default="5432"),
    }
}

# Production email settings, e.g., using SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
