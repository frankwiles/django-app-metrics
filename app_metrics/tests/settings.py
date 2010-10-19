DATABASE_ENGINE='postgresql_psycopg2'
DATABASE_NAME='test_app_metrics'

DEBUG = True 

INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'app_metrics',
        'app_metrics.tests',
]

ROOT_URLCONF = 'app_metrics.tests.urls'
