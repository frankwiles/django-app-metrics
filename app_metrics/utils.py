from django.conf import settings 
from django.utils.importlib import import_module 

from app_metrics.models import Metric, MetricItem 

def create_metric(name=None, slug=None, email_recipients=None, no_email=False, daily=True, weekly=False, monthly=False):
    """ Create a new type of metric to track """ 
    try: 
        new_metric = Metric(
                            name=name, 
                            slug=slug, 
                            no_email=no_email,
                            daily=daily, 
                            weekly=weekly,
                            monthly=monthly)

        new_metric.save()
        for e in email_recipients: 
            new_metric.email_recipients.add(e)

    except: 
        return False 

    return new_metric 

class InvalidMetricsBackend(Exception): pass 
class MetricError(Exception): pass 

def metric(slug=None, num=1):
    """ Increment a metric """ 
   
    backend_string = getattr(settings, 'APP_METRICS_BACKEND', 'app_metrics.backends.db')

    # Attempt to import the backend 
    try: 
        backend = import_module(backend_string)
    except: 
        raise InvalidMetricsBackend("Could not load '%s' as a backend" % backend_string )

    #try: 
    backend.metric(slug, num)
    #except: 
        #raise MetricError('Unable to capture metric')
