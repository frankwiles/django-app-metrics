from app_metrics.models import Metric, MetricItem 

def metric(slug, num=1, **kwargs): 
    """ Record our metric in the database """ 
    met = Metric.objects.get(slug=slug)

    new_metric = MetricItem(metric=met, num=num)
    new_metric.save() 

