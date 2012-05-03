from django.conf import settings
from app_metrics.tasks import statsd_metric_task


def metric(slug, num=1, **kwargs):
    """
    Send metric directly to statsd

    - ``slug`` will be used as the statsd "bucket" string
    - ``num`` increments the counter by that number
    """
    statsd_metric_task.delay(slug, num, **kwargs)
