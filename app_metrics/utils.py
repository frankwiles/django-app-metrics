import datetime 
from django.conf import settings 
from django.utils.importlib import import_module 

from app_metrics.models import Metric, MetricSet, MetricItem 

def get_backend(): 
     return getattr(settings, 'APP_METRICS_BACKEND', 'app_metrics.backends.db')

def create_metric_set(name=None, metrics=None, email_recipients=None, no_email=False, send_daily=True, send_weekly=False, send_monthly=False): 
    """ Create a metric set """ 

    # This should be a NOOP for the mixpanel backend 
    backend = get_backend()
    if backend == 'app_metrics.backends.mixpanel': 
        return 

    try: 
        metric_set = MetricSet(
                            name=name, 
                            no_email=no_email, 
                            send_daily=send_daily,
                            send_weekly=send_weekly,
                            send_monthly=send_monthly)
        metric_set.save()

        for m in metrics: 
            metric_set.metrics.add(m)

        for e in email_recipients: 
            metric_set.email_recipients.add(e)

    except: 
        return False 

    return metric_set 

def create_metric(name, slug): 
    """ Create a new type of metric to track """ 

    # Make this a NOOP for the mixpanel backend 
    backend = get_backend() 
    if backend == 'app_metrics.backends.mixpanel': 
        return 

    # See if this metric already exists 
    existing = Metric.objects.filter(name=name, slug=slug) 

    if existing: 
        return False 
    else: 
        new_metric = Metric(name=name, slug=slug)
        new_metric.save()
        return new_metric 

def get_or_create_metric(name, slug):
    """ Returns the metric with the given name and slug, creating it if necessary """

    backend = get_backend() 
    if backend == 'app_metrics.backends.mixpanel': 
        return 
    
    metric, created = Metric.objects.get_or_create(name=name, slug=slug)
    return metric

class InvalidMetricsBackend(Exception): pass 
class MetricError(Exception): pass 

def metric(slug, num=1, **kwargs):
    """ Increment a metric """ 
   
    backend_string = getattr(settings, 'APP_METRICS_BACKEND', 'app_metrics.backends.db')

    # Attempt to import the backend 
    try: 
        backend = import_module(backend_string)
    except: 
        raise InvalidMetricsBackend("Could not load '%s' as a backend" % backend_string )

    try: 
        backend.metric(slug, num, **kwargs)
    except Metric.DoesNotExist: 
        create_metric(slug=slug, name='Autocreated Metric')

def week_for_date(date): 
    return date - datetime.timedelta(days=date.weekday())

def month_for_date(month): 
    return month - datetime.timedelta(days=month.day-1)

def year_for_date(year): 
    return datetime.date(year.year, 01, 01)

def get_previous_month(date): 
    if date.month == 1: 
        month_change = 12 
    else: 
        month_change = date.month - 1 
    new = date 

    return new.replace(month=month_change)

def get_previous_year(date): 
    new = date 
    return new.replace(year=new.year-1)

