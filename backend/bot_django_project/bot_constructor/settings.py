from pathlib import Path
import os
import sys

PROJECT_ROOT_DIR_NAME = 'tg_bot_constructor'
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# разрешаем импорты также с корня репозитория
sys.path.append(str(BASE_DIR.parent.parent))

SECRET_KEY = 'django-insecure-l^#t200))@a#@3^g7vhy4zk(0)pfg-xfecdr+$@41hw*id)(m6'
# SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DOMAIN_HOST = os.getenv('DOMAIN_HOST', '127.0.0.1:8000')
HOST_PROTOCOL = os.getenv('HOST_PROTOCOL', 'http')

ALLOWED_HOSTS = ['*']

# FIX admin CSRF token issue
# CSRF_TRUSTED_ORIGINS=['https://*.YOUR_DOMAIN.COM']
##  CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*'] doesn't effect so the 'CSRF_TRUSTED_ORIGINS' value is assigned directly as 'http://*.domain.com'



#if DEBUG == True:
#    CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*']
#if not DEBUG == True:
CSRF_TRUSTED_ORIGINS = [f'http://*.{DOMAIN_HOST}', f'https://*.{DOMAIN_HOST}']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'bots',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bot_constructor.urls'

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

WSGI_APPLICATION = 'bot_constructor.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'bot_constructor'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL_NOT_DOMAINED = '/media/'
MEDIA_URL_DOMAINED = f'{HOST_PROTOCOL}://{DOMAIN_HOST}{MEDIA_URL_NOT_DOMAINED}'
MEDIA_URL = MEDIA_URL_DOMAINED

# путь с данными, которые не относятся к исходникам (сгенерированные боты, изображения, видео)
DATA_FILES_ROOT = os.path.join(BASE_DIR, 'data_files')

MEDIA_ROOT = os.path.join(DATA_FILES_ROOT, 'media')

# путь, где лежат созданные пользователем боты
BOTS_DIR = Path(DATA_FILES_ROOT) / 'generated_bots'
BOTS_LOG_DIR = Path(DATA_FILES_ROOT) / 'bot_logs'
PROJECT_LOG_DIR = Path(DATA_FILES_ROOT) / 'project_logs'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}


def check_project_log_dir_exists_and_add_filename(filename: str) -> Path:
    PROJECT_LOG_DIR.mkdir(exist_ok=True)
    return Path(PROJECT_LOG_DIR) / filename


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'main_format': {
            'format': '{asctime} - {levelname} - {message}',
            'style': '{',
        }
    },

    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'main_format',
        },
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': check_project_log_dir_exists_and_add_filename('main_logs.log'),
            'formatter': 'main_format',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['console_handler', 'file_handler'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
