from app_metrics.tasks import librato_metric_task


def metric(name, num=1, **kwargs):
    librato_metric_task.delay(name, num, **kwargs)
