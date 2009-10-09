# Modification tag by Andrew - test is ON
import os.path
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# Django settings for xemple project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('.xemple admin', 'admin@xemple.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'										# 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = os.path.join(PROJECT_PATH, 'db/xemple.db')	# Or path to database file if using sqlite3.
DATABASE_USER = ''												# Not used with sqlite3.
DATABASE_PASSWORD = ''											# Not used with sqlite3.
DATABASE_HOST = ''												# Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''												# Set to empty string for default. Not used with sqlite3.


TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media/')
MEDIA_URL = 'http://127.0.0.1:8000/media'
ADMIN_MEDIA_PREFIX = '/admin-media/'

SECRET_KEY = 'secret'

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (	   
	'django.core.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.doc.XViewMiddleware',
	'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
	'debug_toolbar.middleware.DebugToolbarMiddleware',
)

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
	os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.humanize',
	'django.contrib.flatpages',
	'debug_toolbar',
	'apps.front',
	'apps.manager',
	'apps.client',
	'apps.resources',
	'apps.service',
	'apps.billing',

)


AUTH_PROFILE_MODULE = "client.ClientProfile"
LOGIN_URL = "/manager/login/"
LOGIN_REDIRECT_URL = '/manager/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
APPEND_SLASH = True

from settings_local import *
