"""
Django settings for iportalen project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Used to determined if being run on Openshift, Jenkins or local. Determines DB-connection settings.
ON_PASS = 'OPENSHIFT_REPO_DIR' in os.environ
ON_JENKINS = 'JENKINS_SERVER_IPORTALEN' in os.environ

if ON_PASS:
    ALLOWED_HOSTS = ['*']
    DEBUG = False
    TEMPLATE_DEBUG = False
elif ON_JENKINS:
    ALLOWED_HOSTS = ['*']  # TODO: Should only allow localhost, and what about production?
    DEBUG = False
    TEMPLATE_DEBUG = False
else:
    ALLOWED_HOSTS = ['*']
    DEBUG = True
    TEMPLATE_DEBUG = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^+^i^1i94%j-hi+107xw(vf^mz4hg--#w0mw93+kc#&4vc=#=@'  # TODO: Make use of os.envion on openshift.

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reversion',
    'tags',
    'user_managements',
    'articles',
    'events',
    'organisations',
    'iportalen',
    'storages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

AUTH_USER_MODEL = 'user_managements.IUser'

ROOT_URLCONF = 'iportalen.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(os.path.dirname(BASE_DIR), 'templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'iportalen.wsgi.application'

if ON_PASS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['OPENSHIFT_APP_NAME'],
            'USER': os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
            'PASSWORD': os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
            'HOST': os.environ['OPENSHIFT_MYSQL_DB_HOST'],
            'PORT': os.environ['OPENSHIFT_MYSQL_DB_PORT']
        }
    }
elif ON_JENKINS:
     DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'django_iportalen',
            'USER': 'mysql_jenkins',
            'PASSWORD': '123123123HEJJE',  # Securely generated password.
            'HOST': 'localhost',
            'PORT': '3306'
        }
    }
else:
    from .helpers import get_mysql_credentials
    mysql = get_mysql_credentials()  # Local db credentials.

    DATABASES = {
        'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'django_iportalen',
             'USER': mysql["user"],
             'PASSWORD': mysql["password"],
             'HOST': mysql["host"],
             'PORT': mysql["port"],
        }
    }
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'sv-se'  # en-us

TIME_ZONE = 'Europe/Stockholm'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Target folder of collectstatic.

# Staticfiles settings for local dev environment:
if not ON_PASS:
    STATIC_ROOT = os.path.join(BASE_DIR, "../static/")
    STATIC_URL = "/static/"

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "local_static"),
    )

    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "../media/")

# This is the s3 settings for Openshift.
if ON_PASS:
    STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, "../static/"))
    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")

    AWS_ACCESS_KEY_ID = 'AKIAJSDYCW44P4UNOZQQ'
    AWS_SECRET_ACCESS_KEY = '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'

    # Check if we are on the development instance:
    try:
        os.environ.get('DEVELOPMENT_ENVIRONMENT')
        AWS_STORAGE_BUCKET_NAME = 'iportalen-development'
    except KeyError:
        # This mean we are on the production server. The DEVELOPMENT_ENVIRONMENT variable is set in
        # .openshift/action_hooks/build.sh
        AWS_STORAGE_BUCKET_NAME = 'iportalen-us'
        pass

    S3_URL = 'https://{0}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)
    STATIC_URL = os.environ.get('STATIC_URL', S3_URL + 'static/')

    DEFAULT_FILE_STORAGE = 'iportalen.storage.MediaRootS3BotoStorage'

    STATICFILES_STORAGE = 'iportalen.storage.StaticRootS3BotoStorage'

    MEDIA_URL = os.environ.get('MEDIA_URL', S3_URL + 'client/')

    AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
    }

LOGIN_URL = 'login_view'

# Email settings:
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'noreply@i-portalen.se'
EMAIL_HOST_PASSWORD = '***REMOVED***'
