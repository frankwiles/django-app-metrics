import os

import django

BASE_PATH = os.path.dirname(__file__)

if django.VERSION[:2] >= (1, 3):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    DATABASE_ENGINE = 'sqlite3'
    DATABASE_NAME = ':memory:'

SITE_ID = 1

DEBUG = True

TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'

COVERAGE_MODULE_EXCLUDES = [
    'tests$', 'settings$', 'urls$',
    'common.views.test', '__init__', 'django',
    'migrations', 'djcelery'
]

COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(BASE_PATH, 'coverage')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'app_metrics',
    'app_metrics.tests',
    'djcelery',
    'django_coverage'
]

ROOT_URLCONF = 'app_metrics.tests.urls'

CELERY_ALWAYS_EAGER = True

APP_METRICS_BACKEND = 'app_metrics.backends.db'
APP_METRICS_MIXPANEL_TOKEN = None
APP_METRICS_DISABLED = False

SECRET_KEY = "herp-derp"
