from app_metrics.tasks import librato_metric_task


def metric(name, num, **kwargs):
    librato_metric_task.delay(name, num, **kwargs)
