from ctypes import cast
from email.policy import default
from pathlib import Path
from decouple import config  
from django.utils.timezone import timedelta
import os


BASE_DIR = Path(__file__).resolve().parent.parent

# Variáveis de configuração gerais
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts permitidos
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

# Configuração WSGI padrão (ASGI removido)

USE_LOCAL_DB = config('USE_LOCAL_DB', default=True, cast=bool)

# ============================================================================
# CONFIGURAÇÕES DE BANCO DE DADOS - OTIMIZADAS
# ============================================================================

if USE_LOCAL_DB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('LOCAL_DB_NAME'),
            'USER': config('LOCAL_DB_USER'),
            'PASSWORD': config('LOCAL_DB_PASSWORD'),
            'HOST': config('LOCAL_DB_HOST'),
            'PORT': config('LOCAL_DB_PORT'),
            'OPTIONS': {
                'options': '-c timezone=America/Araguaina',
                'connect_timeout': 30,  # Aumentado de 10 para 30
                'application_name': 'rta_web',
            },
            'CONN_MAX_AGE': 600,  # 10 minutos (era 300 - aumentado)
            'CONN_HEALTH_CHECKS': True,
            'ATOMIC_REQUESTS': False,
            'AUTOCOMMIT': True,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('REMOTE_DB_NAME'),
            'USER': config('REMOTE_DB_USER'),
            'PASSWORD': config('REMOTE_DB_PASSWORD'),
            'HOST': config('REMOTE_DB_HOST'),
            'PORT': config('REMOTE_DB_PORT'),
            'OPTIONS': {
                'options': '-c timezone=America/Araguaina',
                'connect_timeout': 30,  # Aumentado de 10 para 30
                'application_name': 'mobile_sps',
                # Adicionar configurações de pool para estabilidade
                'keepalives': 1,
                'keepalives_idle': 30,
                'keepalives_interval': 10,
                'keepalives_count': 5,
            },
            'CONN_MAX_AGE': 600,  # 10 minutos
            'CONN_HEALTH_CHECKS': True,
            'ATOMIC_REQUESTS': False,
            'AUTOCOMMIT': True,
        },
        "licencas": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("LICENSE_DB_NAME"),  # savexml1
        "USER": config("LICENSE_DB_USER"),
        "PASSWORD": config("LICENSE_DB_PASSWORD"),
        "HOST": config("LICENSE_DB_HOST"),
        "PORT": config("LICENSE_DB_PORT"),
    }
    }


import logging
logger = logging.getLogger("django")
logger.warning("🧠 BASE USADA: %s", "LOCAL" if USE_LOCAL_DB else "REMOTA")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'folhamensal',
    'funcionarios',
    'licencas',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     "core.middleware.BancoMiddleware",
    "core.middleware_auditoria.AuditoriaHttpMiddleware",
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
              
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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

# URLs de autenticação para redirecionar corretamente páginas protegidas (LoginRequired)
LOGIN_URL = "/"
LOGIN_REDIRECT_URL = "/home/"
LOGOUT_REDIRECT_URL = "/"

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

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Araguaina'
USE_TZ = False
USE_I18N = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
