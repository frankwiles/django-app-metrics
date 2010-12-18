DATABASE_ENGINE='sqlite3'
DATABASE_NAME='test_app_metrics'
SITE_ID = 1
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
