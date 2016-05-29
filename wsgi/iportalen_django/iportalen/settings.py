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
ON_CIRCLE = 'ON_CIRCLE' in os.environ
ON_JENKINS = 'JENKINS_SERVER_IPORTALEN' in os.environ


if ON_PASS:
    ALLOWED_HOSTS = ['*']
    DEBUG = False
elif ON_JENKINS:
    ALLOWED_HOSTS = ['*']
    DEBUG = False
else:
    ALLOWED_HOSTS = ['*']
    DEBUG = True


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if not ON_PASS:
    SECRET_KEY = '^+^i^1i94%j-hi+107xw(vf^mz4hg--#w0mw93+kc#&4vc=#=@'
else:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

if ON_PASS:
    ssl = False
    try:
        s = str(os.environ.get('SSL_ENABLED'))
        if s == str("TRUE"):
            ssl = True
    except:
        pass
    if ssl:
        SECURE_SSL_REDIRECT = True
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'speaker_list',
    'iportalen',
    'votings',
    'hero',
    'storages',
    'tags',
    'user_managements',
    'articles',
    'events',
    'organisations',
    'bookings',
    'course_evaluations',
    'faq',
    'django.contrib.sitemaps',
    'rest_framework',
    'django_nose',

)

if not ON_PASS:
    INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)

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

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage'
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
            'NAME': os.environ['JENKINS_DB_NAME'],
            'USER': 'mysql_jenkins',
            'PASSWORD': '123123123HEJJE',  # Securely generated password.
            'HOST': 'localhost',
            'PORT': '3306'
        }
    }
elif ON_CIRCLE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'circle_test',
            'USER': 'ubuntu'
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

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

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


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
}

# Email settings:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # This is a dummy backend which prints emails as a
                                                                  # normal print() statement (i.e. to stdout)
EMAIL_HOST_USER = 'noreply@i-portalen.se'

if ON_PASS:
    send_email = False
    try:
        s = str(os.environ.get('SEND_EMAIL'))
        if s == str('TRUE'):
            send_email = True
    except:
        pass
    if send_email:
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_USE_TLS = True
        EMAIL_HOST = 'smtp.gmail.com'
        EMAIL_PORT = 587
        EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')

SITE_ID = 2

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'level': 'ERROR',
            'handlers': ['console']
        },
        'django.request': {
            'level': 'ERROR',
            'handlers': ['console']
        },
        'django.template': {
            'level': 'ERROR',
            'handlers': ['console']
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console']
        },
        'root': {
            'level': 'ERROR',
            'handlers': ['console']
        },
        'core.handlers': {
            'level': 'ERROR',
            'handlers': ['console']
        },
    },
}


