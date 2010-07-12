""" An example Django settings file for the blog markliu.me"""

import os
import socket

def contains(str, substr):
    if str.find(substr) != -1:
        return True
    else:
        return False

if contains(socket.gethostname(), 'webfaction'):
    LIVEHOST = True
else:
    LIVEHOST = False

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    ('Mark Liu', 'example@email.com'),
)

MANAGERS = ADMINS

if LIVEHOST:
    DEBUG = False

    EMAIL_HOST = 'smtp.webfaction.com'
    EMAIL_HOST_USER = 'user'
    EMAIL_HOST_PASSWORD = 'pass'
    DEFAULT_FROM_EMAIL = 'example@email.com'
    SERVER_EMAIL = 'example@email.com'

    MEDIA_ROOT = '/home/mliu/webapps/media/'
    MEDIA_URL = 'http://markliu.me/media/'
    ADMIN_MEDIA_PREFIX = 'http://markliu.me/media/admin/'

    DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME = 'db_name'     # Or path to database file if using sqlite3.
    DATABASE_USER = 'db_user'             # Not used with sqlite3.
    DATABASE_PASSWORD = 'db_pass'         # Not used with sqlite3.
    DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

else:
    DEBUG = False

    DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME = os.path.join(PROJECT_ROOT, 'mark-liu.db')     # Or path to database file if using sqlite3.
    DATABASE_USER = ''             # Not used with sqlite3.
    DATABASE_PASSWORD = ''         # Not used with sqlite3.
    DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

    # Absolute path to the directory that holds media.
    # Example: "/home/media/media.lawrence.com/"
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')

    # URL that handles the media served from MEDIA_ROOT. Make sure to use a
    # trailing slash if there is a path component (optional in other cases).
    # Examples: "http://media.lawrence.com", "http://example.com/media/"
    MEDIA_URL = 'http://127.0.0.1:8000/media/'

    # URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
    # trailing slash.
    # Examples: "http://foo.com/media/", "/media/".
    ADMIN_MEDIA_PREFIX = '/amedia/'

GOOGLE_WEBMASTER_KEY = 'some_key'

TEMPLATE_DEBUG = DEBUG

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Debug toolbar. This goes after any middleware that encodes the response's content.
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'markliu.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'coltrane',
    'tagging',
    'debug_toolbar',
    'south',
    'disqus',
    'django_twitter_tags',
    'google_webmaster',
)

# INTERNAL_IPS is used for django-debug-toolbar.
INTERNAL_IPS = ('127.0.0.1',)

# For django-debug-toolbar.
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DELICIOUS_USER = 'mliu7'
DELICIOUS_PASSWORD = 'pass'

DISQUS_API_KEY = 'some_key'
DISQUS_WEBSITE_SHORTNAME = 'some_name'
