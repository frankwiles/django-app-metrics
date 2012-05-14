from django.conf import settings
from app_metrics.tasks import statsd_metric_task, statsd_timing_task, statsd_gauge_task


def metric(slug, num=1, **kwargs):
    """
    Send metric directly to statsd

    - ``slug`` will be used as the statsd "bucket" string
    - ``num`` increments the counter by that number
    """
    statsd_metric_task.delay(slug, num, **kwargs)


def timing(slug, seconds_taken, **kwargs):
    """
    Send timing directly to statsd

    - ``slug`` will be used as the statsd "bucket" string
    - ``seconds_taken`` stores the time taken as a float
    """
    statsd_timing_task.delay(slug, seconds_taken, **kwargs)


def gauge(slug, current_value, **kwargs):
    """
    Send timing directly to statsd

    - ``slug`` will be used as the statsd "bucket" string
    - ``current_value`` stores the current value of the gauge
    """
    statsd_gauge_task.delay(slug, current_value, **kwargs)
