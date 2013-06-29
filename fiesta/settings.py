# -*- coding: utf-8 -*-
# Django settings for fiesta project.
import os
location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)
from local_settings import LOCAL_DATABASES

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = LOCAL_DATABASES
#CACHES = {
#    'default': {
#        'BACKEND':
#            'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#        }
#}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'#'en-us'

LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = 'home/e/evesdrearu/fiesta/public_html/fiesta/assets/media'
MEDIA_ROOT = location('assets/media')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = 'home/e/evesdrearu/fiesta/public_html/static' #location('static')
STATIC_ROOT = location('static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'k#r2i&amp;ilyog(j3o7os*^6z0=wx31w51(42+^9$@0naq1f(8io7'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'fiesta_core.middlewares.UnicUser.UnicUserMiddleware'
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'fiesta.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'fiesta.wsgi.application'

from fiesta_core import  FIESTA_MAIN_TEMPLATE_DIR
TEMPLATE_DIRS = (
    FIESTA_MAIN_TEMPLATE_DIR
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'fiesta_core',
    'south',
    'cacheops',
]
from fiesta_core import get_core_apps

INSTALLED_APPS = INSTALLED_APPS + get_core_apps()

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'fiesta_core.core.context_processors.user_metadata',
    'django.core.context_processors.i18n'
    )

AUTHENTICATION_BACKENDS = (
    'fiesta_core.apps.account.auth_backend.CustomUserModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)

CUSTOM_USER_MODEL = 'account.SocialUser'

UNIC_TMP_USER_ID = 'unic_tmp_userid'
TOP_NEWS_LIVETIME = 15 #days

UNIC_TMP_USER_CITY = 'unic_tmp_user_city'


#preview images
PREVIEW_IMG__WIDTH = 337
PREVIEW_IMG_HEIGHT = 300

THUMBNAIL_WIDTH = 80
THUMBNAIL_HEIGHT = 80

#cacheops
CACHEOPS_REDIS = {
    'host': 'localhost',      # сервер redis доступен локально
    'port': 6379,             # порт по умолчанию
    'db': 1,                 # можно выбрать номер БД
    'socket_timeout': 3,
}
CACHEOPS = {
    '*.*': ('just_enable', 60*15),
}

