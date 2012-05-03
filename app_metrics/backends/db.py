from app_metrics.tasks import db_metric_task

def metric(slug, num=1, **kwargs):
    """ Fire a celery task to record our metric in the database """
    db_metric_task.delay(slug, num, **kwargs)
