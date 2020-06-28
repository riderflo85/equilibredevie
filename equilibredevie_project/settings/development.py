import os
from .default import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

new_apps = [
    'django_extensions',
    'debug_toolbar'
]

for app in new_apps:
    INSTALLED_APPS.append(app)

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = ['127.0.0.1']

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
        'PORT': os.environ.get('PORT_DB'),
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci'
        }
    }
}

SUCCES_URL_PAYMENT = 'http://127.0.0.1:8000/order/success?session_id={CHECKOUT_SESSION_ID}'
ERROR_URL_PAYMENT = 'http://127.0.0.1:8000/order/error'
STRIPE_SECRET_KEY = os.environ.get('STRIPE_TEST_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_TEST_PUBLISHABLE_KEY')
STRIPE_PRODUCT = os.environ.get('STRIPE_TEST_PRODUCT')
