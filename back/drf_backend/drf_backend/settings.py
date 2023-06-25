"""
Django settings for drf_backend project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from os.path import join
from pathlib import Path

import matplotlib
matplotlib.use('Agg')

import mne


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False
if 'DJANGO_ENVIRONMENT' in os.environ and os.environ['DJANGO_ENVIRONMENT'] == 'prod':
    env = 'prod'
else:
    env = 'dev'
    DEBUG = True


SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

FRONT_HOST = os.environ['DJANGO_FRONT_HOST']
FRONT_PORT = os.environ['DJANGO_FRONT_PORT']

ALLOWED_HOSTS = [
    FRONT_HOST,
    '127.0.0.1'
]
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:3000',
    'http://localhost:3000',
]

CELERY_BROKER_URL = os.environ['DJANGO_CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['DJANGO_CELERY_BROKER_URL']
CELERY_TASK_ALWAYS_EAGER = False
# allows debugging without celery
if DEBUG:
    CELERY_TASK_ALWAYS_EAGER = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DJANGO_POSTGRES_DATABASE'],
        'USER': os.environ['DJANGO_POSTGRES_USER'],
        'PASSWORD': os.environ['DJANGO_POSTGRES_PASSWORD'],
        'HOST': os.environ['DJANGO_POSTGRES_HOST'],
        'PORT': os.environ['DJANGO_POSTGRES_PORT'],
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'



# Application definition

LANGUAGE_CODE = 'en-us'
USE_TZ = True
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True

WSGI_APPLICATION = 'drf_backend.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'django_rest_passwordreset',
    'data_app',
    'main_app',
    'auth_app',
    'downloads_app',
    'background_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],
    'EXCEPTION_HANDLER': 'drf_backend.utils.custom_exception_handler',
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Urls

ROOT_URLCONF = 'drf_backend.urls'

if env == 'prod':
    STATIC_ROOT = '/django_static/api-static'
    MEDIA_ROOT = '/django_media/media'
    OUT_DIR = '/django_out'
else:
    STATIC_ROOT = join(BASE_DIR, 'static')
    MEDIA_ROOT = join(BASE_DIR, 'media')
    OUT_DIR = join(BASE_DIR, 'out')

STATIC_URL = '/api-static/'
MEDIA_URL = '/media/'
TMP_DIR = join(BASE_DIR, 'tmp')


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'aliceadase@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['DJANGO_EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True

# Logging
if env == 'prod':
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': '/logs/info.log',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }


mne.set_log_level(verbose='ERROR')