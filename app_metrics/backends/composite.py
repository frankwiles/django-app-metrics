from django.conf import settings
from django.utils.importlib import import_module

DEFAULT_BACKENDS = getattr(settings, 'APP_METRICS_COMPOSITE_BACKENDS', [])


def metric(slug, num=1, **kwargs):
    _call_backends('metric', slug, num, **kwargs)


def timing(slug, seconds_taken, **kwargs):
    _call_backends('timing', slug, seconds_taken, **kwargs)


def gauge(slug, current_value, **kwargs):
    _call_backends('gauge', slug, current_value, **kwargs)


def _call_backends(method, slug, value, backends=DEFAULT_BACKENDS, **kwargs):
    for path in backends:
        backend = import_module(path)
        getattr(backend, method)(slug, value, **kwargs)
