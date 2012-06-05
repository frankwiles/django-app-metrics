DATABASE_ENGINE='sqlite3'
DATABASE_NAME='test_app_metrics'
SITE_ID = 1
DEBUG = True
TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'
COVERAGE_MODULE_EXCLUDES = [
        'tests$', 'settings$', 'urls$',
        'common.views.test', '__init__', 'django',
        'migrations', 'djcelery']

INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'app_metrics',
        'app_metrics.tests',
        'djcelery',
]

ROOT_URLCONF = 'app_metrics.tests.urls'

CELERY_ALWAYS_EAGER = True

APP_METRICS_BACKEND = 'app_metrics.backends.db'
APP_METRICS_MIXPANEL_TOKEN = None
APP_METRICS_DISABLED = False
