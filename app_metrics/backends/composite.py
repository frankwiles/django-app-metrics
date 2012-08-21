from django.conf import settings
from django.utils.importlib import import_module

BACKENDS = dict((
    ("db", "app_metrics.backends.db"),
    ("librato", "app_metrics.backends.librato_backend"),
    ("mixpanel", "app_metrics.backends.mixpanel"),
    ("redis", "app_metrics.backends.redis"),
    ("statsd", "app_metrics.backends.statsd"),
) + getattr(settings, 'APP_METRICS_BACKENDS', ()))

DEFAULT_BACKENDS = getattr(settings, 'APP_METRICS_DEFAULT_BACKENDS', [])


def metric(slug, num=1, **kwargs):
    _call_backends('metric', slug, num, **kwargs)


def timing(slug, seconds_taken, **kwargs):
    _call_backends('timing', slug, seconds_taken, **kwargs)


def gauge(slug, current_value, **kwargs):
    _call_backends('gauge', slug, current_value, **kwargs)


def _call_backends(method, slug, value, backends=DEFAULT_BACKENDS, **kwargs):
    for backend_name in backends:
        path = BACKENDS.get(backend_name)
        if path:
            backend = import_module(path)
            getattr(backend, method)(slug, value, **kwargs)
