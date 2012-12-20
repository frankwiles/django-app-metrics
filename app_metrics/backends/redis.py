# Backend to store info in Redis
from django.conf import settings
from app_metrics.tasks import redis_metric_task, redis_gauge_task

def metric(slug, num=1, properties={}):
    redis_metric_task.delay(slug, num, **properties)

def timing(slug, seconds_taken, **kwargs):
    # No easy way to do this with redis, so this is a no-op
    pass

def gauge(slug, current_value, **kwargs):
    redis_gauge_task.delay(slug, current_value, **kwargs)

