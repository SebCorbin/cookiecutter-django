from __future__ import absolute_import, division, print_function

import copy
import os
from datetime import timedelta
from importlib import import_module

import django
import six
from django.utils.log import DEFAULT_LOGGING


"""
Django settings for {{cookiecutter.django_project_name}} project.

Generated by 'django-admin startproject' using Django {{cookiecutter.django_ver}}.

For more information on this file, see
https://docs.djangoproject.com/en/{{cookiecutter.django_ver_1}}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{cookiecutter.django_ver_1}}/ref/settings/
"""


def as_col(value, separators=None, final_type=None, **kw):
    if final_type is None:
        final_type = list
    if separators is None:
        separators = ['-|_', '_|-', '___', ',', ';', '|']
    if isinstance(value, six.string_types):
        assert(len(separators))
        while separators:
            try:
                separator = separators.pop(0)
            except IndexError:
                break
            if separator in value:
                break
        value = final_type(value.split(separator))
        if final_type is not list:
            value = final_type(value)
    return value


def as_int(value, **kw):
    if value not in ['', None]:
        value = int(value)
    return value


def as_bool(value, asbool=True):
    if isinstance(value, six.string_types):
        if value and asbool:
            low = value.lower().strip()
            if low in [
                'false', 'non', 'no', 'n', 'off', '0', '',
            ]:
                return False
            if low in [
                'true', 'oui', 'yes', 'y', 'on', '1',
            ]:
                return True
    return bool(value)


def locals_settings_update(locs_, d=None):
    if d is None:
        d = {}
    for a, b in six.iteritems(d):
        if a in [
            '__name__', '__doc__', '__package__',
            '__loader__', '__spec__', '__file__',
            '__cached__', '__builtins__'
        ]:
            continue
        locs_[a] = b
    return locs_, d.get('__name__', '').split('.')[-1]


def filter_globals(locs_, d=None):
    if d is None:
        d = {}
    return locals_settings_update({}, globals())[0]


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
{{cookiecutter.lname.upper()}}_DIR = PROJECT_DIR
SRC_DIR = os.path.dirname(PROJECT_DIR)
BASE_DIR = os.path.dirname(SRC_DIR)
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
PRIVATE_DIR = os.path.join(BASE_DIR, 'private')
PROJECT_NAME = os.path.basename(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/{{cookiecutter.django_ver_1}}/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = None

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #
    'apptest'
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
{%- if cookiecutter.django_ver[0]|int < 2 %}
# django 1/2 compat
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
{%- endif %}
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = PROJECT_NAME + '.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join({{cookiecutter.lname.upper()}}_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'

# Database
# https://docs.djangoproject.com/en/{{cookiecutter.django_ver_1}}/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': {%- if 'postgis' in cookiecutter.db_mode.lower() %}
            'django.contrib.gis.db.backends.postgis'
            {%- elif 'postgres' in cookiecutter.db_mode.lower() %}
            'django.db.backends.postgresql_psycopg2'
            {%- else %}
            'django.db.backends.{{cookiecutter.db_mode.lower()}}'
            {%- endif %}
    }
}
DEFAULT_DB = DATABASES['default']
db_opts = (
    ('mysql', {
        'NAME': ('MYSQL_DATABASE',),
        'USER': ('MYSQL_USER',),
        'PASSWORD': ('MYSQL_PASSWORD',),
        'HOST': ('MYSQL_HOST',),
        'PORT': ('MYSQL_PORT',),
    }),
    ('post', {
        'NAME': ('POSTGRES_DB',),
        'USER': ('POSTGRES_USER',),
        'PASSWORD': ('POSTGRES_PASSWORD',),
        'HOST': ('POSTGRES_HOST',),
        'PORT': ('POSTGRES_PORT',),
    }),
    ('general', {
        'NAME': ('DATABASE_NAME', 'DB_NAME',),
        'USER': ('DATABASE_USER', 'DB_USER',),
        'HOST': ('DATABASE_HOST', 'DB_HOST',),
        'PORT': ('DATABASE_PORT', 'DB_PORT',),
        'PASSWORD': ('DATABASE_PORT', 'DB_PASSWORD',),
    }),
)
db_opts_dict = dict(db_opts)
db_opts_k = 'general'
for k, values in db_opts:
    if k in DEFAULT_DB['ENGINE']:
        db_opts_k = k
        break
for v, envvars in db_opts_dict[db_opts_k].items():
    for envvar in envvars + db_opts_dict['general'][v]:
        try:
            DEFAULT_DB.setdefault(v,  os.environ[envvar])
            break
        except KeyError:
            pass

DEFAULT_DB.setdefault('HOST', 'db')
DEFAULT_DB.setdefault('PORT', '')

# Password validation
# https://docs.djangoproject.com/en/{{cookiecutter.django_ver_1}}/ref/settings/#auth-password-validators

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
{% if cookiecutter.user_model %}
AUTH_USER_MODEL = '{{cookiecutter.user_model}}'
{% endif %}
# LOGIN_URL = 'login'
# LOGIN_REDIRECT_URL = 'home'
# LOGOUT_URL = 'logout'

# Internationalization
# https://docs.djangoproject.com/en/{{cookiecutter.django_ver_1}}/topics/i18n/
LANGUAGE_CODE = '{{cookiecutter.language_code}}'
TIME_ZONE = '{{cookiecutter.tz}}'
USE_I18N = {{ cookiecutter['use_i18n'] and 'True' or 'False'}}
USE_L10N =  {{ cookiecutter['use_l10n'] and 'True' or 'False'}}
USE_TZ =  {{ cookiecutter['use_tz'] and 'True' or 'False'}}
LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locales'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/{{cookiecutter.django_ver_1}}/howto/static-files/
STATIC_URL = '{{cookiecutter.statics_uri}}/'
STATICFILES_DIRS = (
    os.path.join({{cookiecutter.lname.upper()}}_DIR, 'static'),
)
STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')
MEDIA_URL = '{{cookiecutter.media_uri}}/'
MEDIA_ROOT = os.path.join(PUBLIC_DIR, 'media')

# Just to be easily override by children conf files.
LOGGING = copy.deepcopy(DEFAULT_LOGGING)

# Cache settings
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CORS_ORIGIN_ALLOW_ALL = True

# Mail
EMAIL_HOST = 'mailcatcher'
EMAIL_PORT = 1025

# Make django configurable via environment
SETTINGS_ENV_PREFIX = 'DJANGO__'
# Those settings will throw a launch failure in deploy envs
# if they are not explicitly set
EXPLICIT_ENV_VARS = ['SECRET_KEY']
ENV_VARS = EXPLICIT_ENV_VARS + [
    'EMAIL_HOST',
    'EMAIL_PORT',
    'EMAIL_USE_TLS',
    'EMAIL_HOST_USER',
    'EMAIL_HOST_PASSWORD',
    'DEFAULT_FROM_EMAIL']
DJANGO_ENV_VARS = {}

# Scan environ for django configuration items
for i, val in os.environ.items():
    # Bring back prefixed env vars
    # eg DJANGO__SECRET_KEY to SECRET_KEY form.
    if i.startswith(SETTINGS_ENV_PREFIX):
        s = SETTINGS_ENV_PREFIX.join(i.split(SETTINGS_ENV_PREFIX)[1:])
        DJANGO_ENV_VARS[s] = val
    #
    # Look also at the environ Root for explicit env vars
    #  Please note that prefixed value will always have
    #  the higher priority (DJANGO__FOO vs FOO)
    for s in ENV_VARS:
        if s not in DJANGO_ENV_VARS:
            try:
                DJANGO_ENV_VARS[s] = os.environ[s]
            except KeyError:
                pass

# export back DJANGO_ENV_VARS dict as django settings
globs = globals()
for s, val in six.iteritems(DJANGO_ENV_VARS):
    globs[s] = val


def check_explicit_settings(globs=None):
    '''
    verify that some vars are explicitly defined
    '''
    locs_, env = locals_settings_update(locals(), globs)
    for i in EXPLICIT_ENV_VARS:
        try:
            _ = locs_[i]  #noqa
        except KeyError:
            raise Exception('{0} django settings is not defined')
    globals().update(locs_)
    return locs_, filter_globals(globals()), env


def post_process_settings(globs=None):
    '''
    Make intermediary processing on settings like:
        - checking explicit vars
        - tranforming vars which can come from system environment as strings
          in their final values as django settings
    '''
    locs_, globs, env = check_explicit_settings(globs)
    for setting, func, fkw in (
        ('EMAIL_PORT', as_int, {}),
        ('EMAIL_USE_TLS', as_bool, {}),
        ('CORS_ORIGIN_ALLOW_ALL', as_bool, {}),
        ('CORS_ORIGIN_WHITELIST', as_col, {'final_type': tuple}),
        ('ALLOWED_HOSTS', as_col, {}),
    ):
        try:
            locs_[setting]
        except KeyError:
            continue
        locs_[setting] = func(locs_[setting], **fkw)
    {% if cookiecutter.with_sentry -%}SENTRY_DSN = locs_.setdefault('SENTRY_DSN', '')
    SENTRY_RELEASE = locs_.setdefault('SENTRY_RELEASE', 'prod')
    INSTALLED_APPS = locs_.setdefault('INSTALLED_APPS', tuple())
    SENTRY_TAGS = locs_.pop('SENTRY_TAGS', None)
    if SENTRY_DSN:
        if 'raven.contrib.django.raven_compat' not in INSTALLED_APPS:
            locs_['INSTALLED_APPS'] = (
                type(
                    locs_['INSTALLED_APPS']
                )(['raven.contrib.django.raven_compat']) +
                locs_['INSTALLED_APPS'])
        RAVEN_CONFIG = locs_.setdefault('RAVEN_CONFIG', {})
        RAVEN_CONFIG.setdefault('release', SENTRY_RELEASE)
        RAVEN_CONFIG['dsn'] = SENTRY_DSN
        RAVEN_CONFIG.setdefault(
            'transport',
            'raven.transport.requests.RequestsHTTPTransport')
        # If you are using git, you can also automatically
        # configure the release based on the git info.
        LOGGING = locs_.setdefault('LOGGING', copy.deepcopy(DEFAULT_LOGGING))
        LOGGING['disable_existing_loggers'] = True
        LOGGING.setdefault('handlers', {}).update({
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',  #noqa
            }})
        root = LOGGING.setdefault('root', {})
        root['handlers'] = ['sentry']
        if SENTRY_TAGS and isinstance(SENTRY_TAGS, six.string_types):
            locs_['SENTRY_TAGS'] = {}
            for a in SENTRY_TAGS.split(','):
                tag, val = a.split(':')[0], ':'.join(a.split(':')[1:])
                if not val:
                    val, tag = tag, 'general'
                locs_['SENTRY_TAGS'][tag] = val
        if 'DEPLOY_ENV' in locs_:
            locs_['RAVEN_CONFIG']['environment'] = locs_['DEPLOY_ENV']
    {%- endif %}
    globals().update(locs_)
    return locs_, filter_globals(globals()), env


def set_prod_settings(globs):
    '''
    Additional post processing of settings only ran on hosted environments
    '''
    locs_, env = locals_settings_update(locals(), globs)
    SERVER_EMAIL = locs_.setdefault(
        'SERVER_EMAIL',
        '{env}-{{cookiecutter.lname}}@{{cookiecutter.tld_domain}}'.format(env=env))
    locs_.setdefault('ADMINS', [('root', SERVER_EMAIL)])
    locs_.setdefault('EMAIL_HOST', 'localhost')
    locs_.setdefault('DEFAULT_FROM_EMAIL', SERVER_EMAIL)
    ALLOWED_HOSTS = locs_.setdefault('ALLOWED_HOSTS', [])
    CORS_ORIGIN_WHITELIST = locs_.setdefault(
        'CORS_ORIGIN_WHITELIST', tuple())
    # those settings by default are empty, we need to handle this case
    if not CORS_ORIGIN_WHITELIST:
        locs_['CORS_ORIGIN_WHITELIST'] = (
            '{env}-{{cookiecutter.lname}}.{{cookiecutter.tld_domain}}'.format(env=env),  #noqa
            '.{{cookiecutter.tld_domain}}')
    if not ALLOWED_HOSTS:
        locs_['ALLOWED_HOSTS'] = [
            '{env}-{{cookiecutter.lname}}.{{cookiecutter.tld_domain}}'.format(env=env),  # noqa
            '.{{cookiecutter.tld_domain}}']
    globals().update(locs_)
    return locs_, filter_globals(globals()), env
