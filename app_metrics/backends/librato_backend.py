from app_metrics.tasks import librato_metric_task


def metric(slug, num=1, **kwargs):
    librato_metric_task.delay(slug, num, metric_type="counter", **kwargs)


def timing(slug, seconds_taken, **kwargs):
    """not implemented"""


def gauge(slug, current_value, **kwargs):
    librato_metric_task.delay(slug, current_value, metric_type="gauge",
                              **kwargs)
