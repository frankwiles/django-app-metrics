from celery.decorators import task 

from app_metrics.models import Metric, MetricItem 

def metric(slug, num=1, **kwargs): 
    """ Fire a celery task to record our metric in the database """ 
    db_metric_task.delay(slug, num, **kwargs) 

@task 
def db_metric_task(slug, num=1, **kwargs): 
    met = Metric.objects.get(slug=slug)

    new_metric = MetricItem.objects.create(metric=met, num=num)

