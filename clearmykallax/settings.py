"""
Django settings for clearmykallax project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'asdf')

DEBUG = os.getenv('DJANGO_DEBUG', 'true').upper() in {'TRUE', 'YES', 'Y'}

ALLOWED_HOSTS = [host for x in os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',') if (host := x.strip())]


DEFAULT_FROM_EMAIL = os.getenv('DJANGO_DEFAULT_FROM_EMAIL', 'games@bmispelon.rocks')

if 'DJANGO_EMAIL_HOST' in os.environ:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    try:
        host, port = os.environ['DJANGO_EMAIL_HOST'].split(':')
    except ValueError:
        EMAIL_HOST = os.environ['DJANGO_EMAIL_HOST']
    else:
        EMAIL_HOST = host
        EMAIL_PORT = int(port)

    EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD', '')
    EMAIL_USE_TLS = os.getenv('DJANGO_EMAIL_USE_TLS', 'FALSE').upper() in {'TRUE', 'YES', 'Y'}
    EMAIL_USE_SSL = os.getenv('DJANGO_EMAIL_USE_SSL', 'FALSE').upper() in {'TRUE', 'YES', 'Y'}
    EMAIL_TIMEOUT = int(os.getenv('DJANGO_EMAIL_TIMEOUT', '30'))
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'import_export',

    'games',
    'signups',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'sesame.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if os.getenv('DJANGO_USE_WHITENOISE', 'no').upper() in {'YES', 'TRUE', 'Y'}:
    # insert whitenoise middleware just after django's security middleware
    MIDDLEWARE.insert(
        MIDDLEWARE.index('django.middleware.security.SecurityMiddleware'),
        'whitenoise.middleware.WhiteNoiseMiddleware'
    )

ROOT_URLCONF = 'clearmykallax.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'clearmykallax' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {'formtools': 'clearmykallax.templatetags.formtools'},
        },
    },
]

WSGI_APPLICATION = 'clearmykallax.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {'default': dj_database_url.config(default='postgres:///clearmykallax')}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'sesame.backends.ModelBackend',
]

LOGIN_URL = 'signups:send-magic-link'
LOGOUT_REDIRECT_URL = 'landing'


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Oslo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = BASE_DIR / '_collectedstatic'
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'clearmykallax' / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


if 'DJANGO_SECURE_PROXY_SSL_HEADER' in os.environ:
    SECURE_PROXY_SSL_HEADER = (os.environ['DJANGO_SECURE_PROXY_SSL_HEADER'], 'https')
SECURE_SSL_REDIRECT = os.getenv('DJANGO_SECURE_SSL_REDIRECT', 'FALSE').upper() in {'TRUE', 'YES', 'Y'}
