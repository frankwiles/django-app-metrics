try:
    from celery.task import task
except ImportError:
    from celery.decorators import task

from django.conf import settings

import librato
from librato.metrics import Gauge, Counter


@task
def librato_metric_task(name, num, attributes=None, metric_type="gauge",
                        **kwargs):
    connection = librato.connect(settings.APP_METRICS_LIBRATO_USER,
                                 settings.APP_METRICS_LIBRATO_TOKEN)

    if metric_type == "counter":
        metric = Counter(connection, name, attributes=attributes)
    else:
        metric = Gauge(connection, name, attributes=attributes)

    metric.add(num, source=settings.APP_METRICS_LIBRATO_SOURCE)
