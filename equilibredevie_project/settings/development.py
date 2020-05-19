import os
from .default import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS.append('django_extensions')

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'NAME': os.environ.get('NAME_DB'),
        'USER': os.environ.get('USER_DB'),
        'PASSWORD': os.environ.get('PWD_DB'),
        'HOST': os.environ.get('HOST_DB'),
        'PORT': os.environ.get('PORT_DB')
    }
}

STRIPE_SECRET_KEY = os.environ.get('STRIPE_TEST_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_TEST_PUBLISHABLE_KEY')
