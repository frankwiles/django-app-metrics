from app_metrics.models import Metric, MetricItem 

def metric(slug=None, num=1): 
    """ Record our metric in the database """ 
    met = Metric.objects.get(slug=slug)

    new_metric = MetricItem(metric=met, num=num)
    new_metric.save() 

