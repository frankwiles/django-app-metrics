from django.conf import settings 

from app_metrics.models import Metric, MetricItem 

def create_metric(name=None, slug=None, email_recipients=None, no_email=None, daily=True, weekly=False, monthly=False):
    """ Create a new type of metric to track """ 
    try: 
        new_metric = Metric(
                            name=name, 
                            slug=slug, 
                            email_recipients=email_recipients, 
                            no_email=no_email,
                            daily=daily, 
                            weekly=weekly,
                            monthly=monthly)
        new_metric.save()
    except: 
        return False 

    return new_metric 

class InvalidMetricsBackend(Exception): pass 
class MetricError(Exception): pass 

def metric(slug=None, count=1):
    """ Increment a metric """ 
    
    # Attempt to import the backend 
    try: 
        backend_string = settings.get('APP_METRICS_BACKEND', 'app_metrics.backends.db')
        backend = __import__(backend_string)

    except: 
        raise InvalidMetricsBackend("Could not load '%s' as a backend" % backend_string )

    try: 
        backend.metric(slug, count)
    except: 
        raise MetricError('Unable to capture metric')
