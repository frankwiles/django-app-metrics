from app_metrics.tasks import db_metric_task, db_gauge_task


def metric(slug, num=1, **kwargs):
    """ Fire a celery task to record our metric in the database """
    db_metric_task.delay(slug, num, **kwargs)


def timing(slug, seconds_taken, **kwargs):
    # Unsupported, hence the noop.
    pass


def gauge(slug, current_value, **kwargs):
    """Fire a celery task to record the gauge's current value in the database."""
    db_gauge_task.delay(slug, current_value, **kwargs)
