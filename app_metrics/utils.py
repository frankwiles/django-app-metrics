from contextlib import contextmanager
import datetime
import time
from django.conf import settings
from django.utils.importlib import import_module

from app_metrics.exceptions import InvalidMetricsBackend, TimerError
from app_metrics.models import Metric, MetricSet

def get_backend():
     return getattr(settings, 'APP_METRICS_BACKEND', 'app_metrics.backends.db')

def should_create_models(backend=None):
    if backend is None:
        backend = get_backend()

    return backend == 'app_metrics.backends.db'


def create_metric_set(name=None, metrics=None, email_recipients=None,
        no_email=False, send_daily=True, send_weekly=False,
        send_monthly=False):
    """ Create a metric set """

    # This should be a NOOP for the non-database-backed backends
    if not should_create_models():
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

    # This should be a NOOP for the non-database-backed backends
    if not should_create_models():
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
    """
    Returns the metric with the given name and slug, creating
    it if necessary
    """

    # This should be a NOOP for the non-database-backed backends
    if not should_create_models():
        return

    metric, created = Metric.objects.get_or_create(name=name, slug=slug)
    return metric


def import_backend():
    backend_string = get_backend()

    # Attempt to import the backend
    try:
        backend = import_module(backend_string)
    except:
        raise InvalidMetricsBackend("Could not load '%s' as a backend" % backend_string )

    return backend


def metric(slug, num=1, **kwargs):
    """ Increment a metric """
    backend = import_backend()

    try:
        backend.metric(slug, num, **kwargs)
    except Metric.DoesNotExist:
        create_metric(slug=slug, name='Autocreated Metric')


class Timer(object):
    """
    An object for manually controlling timing. Useful in situations where the
    ``timing`` context manager will not work.

    Usage::

        timer = Timer()
        timer.start()

        # Do some stuff.

        timer.stop()

        # Returns a float of how many seconds the logic took.
        timer.elapsed()

        # Stores the float of how many seconds the logic took.
        timer.store()

    """
    def __init__(self):
        self._start = None
        self._elapsed = None

    def timestamp(self):
        return time.time()

    def start(self):
        if self._start is not None:
            raise TimerError("You have already called '.start()' on this instance.")

        self._start = time.time()

    def stop(self):
        if self._start is None:
            raise TimerError("You must call '.start()' before calling '.stop()'.")

        self._elapsed = time.time() - self._start
        self._start = None

    def elapsed(self):
        if self._elapsed is None:
            raise TimerError("You must call '.stop()' before trying to get the elapsed time.")

        return self._elapsed

    def store(self, slug):
        backend = import_backend()
        backend.timing(slug, self.elapsed())


@contextmanager
def timing(slug):
    """
    A context manager to recording how long some logic takes & sends it off to
    the backend.

    Usage::

        with timing('create_event'):
            # Your code here.
            # For example, create the event & all the related data.
            event = Event.objects.create(
                title='Coffee break',
                location='LPT',
                when=datetime.datetime(2012, 5, 4, 14, 0, 0)
            )
    """
    timer = Timer()
    timer.start()
    yield
    timer.stop()
    timer.store(slug)


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

