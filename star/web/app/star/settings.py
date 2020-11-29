"""
Django settings for star project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xxxxx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'home.apps.HomeConfig',
    'edge.apps.Tx2Config',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    
    'bootstrap3',
    'channels',
    'django_cron',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CRON_CLASSES = [
    "cron.update_db.UpdateHistory",
    "cron.purge_db.PurgeOldHistory",
    "cron.check_disk.LimitDiskUsage",
    "cron.update_light.UpdateLight",
]
DJANGO_CRON_DELETE_LOGS_OLDER_THAN = 7 # days

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'star.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates') ],
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

WSGI_APPLICATION = 'star.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'ENFORCE_SCHEMA': True,
        'NAME': 'star-db',
        'HOST': 'db',
        'PORT': 27017,
    }
}

# Caches settings
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# channels settings
ASGI_APPLICATION = "star.routing.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'account/static'), ]

# login settings
LOGIN_URL = 'account_login'
LOGOUT_URL = 'home'
LOGIN_ERROR_URL = 'home'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home' 

# session settings
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"   # ref: Caches settings
SESSION_COOKIE_AGE = 60 * 60 * 24 # seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ddl.itlab@gmail.com'
EMAIL_HOST_PASSWORD = 'xxxxx'

# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, "account/emails")

SITE_ID = 1
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[ITLab SSL] "

# sed -i "s|return uri|return 'https://ssl.itlab.ee.ncku.edu.tw/' + uri.partition('//')[2].partition('/')[2]|" /usr/local/lib/python3*/site-packages/allauth/utils.py

# Settings for django-bootstrap3
BOOTSTRAP3 = {
    "jquery_url": "/static/home/plugin/jquery-3.3.1.min.js",
    "css_url": "/static/home/plugin/bootstrap.min-3.3.7.css",
    "javascript_url": "/static/home/plugin/bootstrap.min-3.3.7.js",
}

# Global Configs

SETUP_MSG = '\
#### Edge Service Parameters ####\\n\
SSH_USER=limited-user\\n\
SSH_PORT=62422\\n\
SSH_NETLOC=ssl.itlab.ee.ncku.edu.tw\\n\
\\n\
RTMP_REMOTE_NETLOC=nginx-rtmp:1935\\n\
RTMP_PATH=/itlab/\\n\
\\n\
WS_REMOTE_NETLOC=web:8001\\n\
WS_PATH=/ws/edge/device/\\n\
\\n\
RTMP_NETLOC=localhost:65000\\n\
WS_NETLOC=localhost:65001'

SSH_KEY_PATH = '/authorized_keys'

HLS_URL = 'https://ssl.itlab.ee.ncku.edu.tw/hls/'
RTMP_DROP_URL = 'http://nginx-rtmp/control/drop/publisher?app=itlab&name={}'

VOD_URL = 'https://ssl.itlab.ee.ncku.edu.tw/vod/'
VOD_DIR = '/media/data/record'
VOD_EXT = '.mp4'
VOD_LEN = 15 # minutes

INFO_TIMEOUT = 30 # seconds
INFO_TIMESTR = '%Y-%m-%d %H:%M:%S %z'
INFO_POSTFIX = '_info'

CHANNEL_POSTFIX = '_channel'

API_TOKEN_TIMEOUT = 10 * 60 # seconds


# Cron Jobs (run with crontab)

PURGE_DB_AT = ['06:11']
PURGE_HISTORY_OLDER_WEEKS = 365 / 7 # > 1 year

CHECK_DISK_USAGE_AT = ['07:11']
MAX_DISK_USAGE_PERCENT = 80
DEL_OLDEST_VOD_PERCENT = 20

UPDATE_AT = ['00:00']
UPDATE_HISTORY_EVERY_MINS = 15
UPDATE_LIGHT_EVERY_MINS = 15
