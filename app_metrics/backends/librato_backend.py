from app_metrics.tasks import librato_metric_task


def metric(slug, num=1, async=True, **kwargs):
    if async:
        librato_metric_task.delay(slug, num, metric_type="counter", **kwargs)
    else:
        librato_metric_task(slug, num, metric_type="counter", **kwargs)


def timing(slug, seconds_taken, async=True, **kwargs):
    """not implemented"""


def gauge(slug, current_value, async=True, **kwargs):
    if async:
        librato_metric_task.delay(slug, current_value, metric_type="gauge",
                                  **kwargs)
    else:
        librato_metric_task(slug, current_value, metric_type="gauge", **kwargs)
