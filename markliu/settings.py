# Django settings for the blog markliu.me

import os
import socket
import sys

import dj_database_url


# Test to see if local_settings exists. If it doesn't exist then this is on the live host.
if os.path.isfile('local_settings.py'):
    LIVEHOST = False
else:
    LIVEHOST = True


S3_URL = 'https://s3.amazonaws.com/markliu/'
USE_STATICFILES = False
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    ('Mark Liu', 'markwayneliu@gmail.com'),
)

MANAGERS = ADMINS

if LIVEHOST:
    DEBUG = os.environ.get('DJANGO_DEBUG', '').lower() == "true"

    # Heroku settings: https://devcenter.heroku.com/articles/django#database-settings
    DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

    # Django storages
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    USE_STATICFILES = True

    # URL prefix for static files.
    STATIC_URL = S3_URL

    GOOGLE_WEBMASTER_KEY = os.environ['GOOGLE_WEBMASTER_KEY']
    SECRET_KEY = os.environ['SECRET_KEY'] 
    DISQUS_API_KEY = os.environ['DISQUS_API_KEY'] 
    DELICIOUS_PASSWORD = os.environ['DELICIOUS_PASSWORD'] 

else:
    DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJECT_ROOT, 'mark-liu.db'),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

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

    STATIC_URL = '/media/'

    # Django storages
    AWS_ACCESS_KEY_ID = '' # To use this to upload files to S3, this should be defined in local_settings.py
    AWS_SECRET_ACCESS_KEY = '' # To use this to upload files to S3, this should be defined in local_settings.py
    if 'collectstatic' in sys.argv:
        USE_STATICFILES = True


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

# Make this unique, and don't share it with anybody.

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',      
]


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
    'south',
    'coltrane',
    'tagging',
    'debug_toolbar',
    'disqus',
    'django_twitter_tags',
    'google_webmaster',
    'django_posterous',
)

# INTERNAL_IPS is used for django-debug-toolbar.
#INTERNAL_IPS = ('127.0.0.1',)

# For django-debug-toolbar.
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DELICIOUS_USER = 'mliu7'

DISQUS_WEBSITE_SHORTNAME = 'markliusblog'

DJANGO_POSTEROUS_SITE_NAME = 'wiscospike'   # The site name of your posterous site (yoursitename.posterous.com)
DJANGO_POSTEROUS_BLOG_MODULE = 'coltrane'   # The module of your django blog
DJANGO_POSTEROUS_BLOG_MODEL = 'Entry'       # The model where the blog posts are stored
DJANGO_POSTEROUS_TITLE_FIELD = 'title'      # The name of the title field within your blog model
DJANGO_POSTEROUS_BODY_FIELD = 'body_html'   # The name of the field where your post will be stored
DJANGO_POSTEROUS_DATE_FIELD = 'pub_date'    # The name of the field where the date of the post will be stored
DJANGO_POSTEROUS_AUTHOR_FIELD = 'author'    # The name of the field where the author of the post will be stored


##############################################################################
# Django-storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
if USE_STATICFILES:
    STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
AWS_STORAGE_BUCKET_NAME = 'markliu'
AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {
    'Cache-Control': 'max-age=3600',
}

try:
    from local_settings import *
except ImportError:
    pass
