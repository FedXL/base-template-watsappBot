import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent.parent
files_and_dirs = os.listdir(BASE_DIR)

load_dotenv(BASE_DIR / '.env')
SECRET_KEY = os.getenv('SECRET_KEY')
VERSION = os.getenv('VERSION')




if VERSION == 'deploy':
    DEBUG = True
    ALLOWED_HOSTS = ['nurbot.kz','www.nurbot.kz']
    CSRF_TRUSTED_ORIGINS = ['https://nurbot.kz', 'https://www.nurbot.kz']
    HOST_PREFIX = 'https://nurbot.kz'
elif VERSION == 'development':
    DEBUG = True
    HOST_PREFIX = ''
else:
    raise ValueError('VERSION can be either DEV or DEPLOY')

WSGI_APPLICATION = 'stations.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'api_backend.apps.ApiBackendConfig',
    'clients.apps.ClientsConfig',
    'shop.apps.ShopConfig',
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

ROOT_URLCONF = 'stations.urls'

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

WSGI_APPLICATION = 'stations.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),

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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if VERSION == 'deploy':
    FORCE_SCRIPT_NAME = '/water/'
    BASE_URL = '/water'
    MEDIA_URL = BASE_URL + '/media/'
    STATIC_URL =BASE_URL + '/static/'
elif VERSION == 'development':
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'
else:
    raise ValueError('VERSION can be either development or deploy')

STATIC_ROOT =  '/var/www/static'
MEDIA_ROOT = '/var/www/media'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
TIME_ZONE='Asia/Almaty'

LANGUAGE_CODE= 'ru-ru'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',  # Set to INFO to reduce verbosity
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',  # Set to WARNING to reduce database logs
            'propagate': False,
        },
    },
}



