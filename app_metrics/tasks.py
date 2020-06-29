import base64
import json
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import datetime
from decimal import Decimal

try:
    from celery.task import task
except ImportError:
    from celery.decorators import task

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from app_metrics.models import Metric, MetricItem, Gauge

# For statsd support
try:
    # Not required. If we do this once at the top of the module, we save
    # ourselves the pain of importing every time the task fires.
    import statsd
except ImportError:
    statsd = None

# For redis support
try:
    import redis
except:
    redis = None

# For librato support
try:
    import librato
    from librato.metrics import Gauge as LibratoGauge
    from librato.metrics import Counter as LibratoCounter
except ImportError:
    librato = None


class MixPanelTrackError(Exception):
    pass

# DB Tasks

@task
def db_metric_task(slug, num=1, **kwargs):
    met = Metric.objects.get(slug=slug)
    MetricItem.objects.create(metric=met, num=num)


@task
def db_gauge_task(slug, current_value, **kwargs):
    gauge, created = Gauge.objects.get_or_create(slug=slug, defaults={
        'name': slug,
        'current_value': current_value,
    })

    if not created:
        gauge.current_value = current_value
        gauge.save()


def _get_token():
    token = getattr(settings, 'APP_METRICS_MIXPANEL_TOKEN', None)

    if not token:
        raise ImproperlyConfigured("You must define APP_METRICS_MIXPANEL_TOKEN when using the mixpanel backend.")
    else:
        return token

# Mixpanel tasks

@task
def mixpanel_metric_task(slug, num, properties=None, **kwargs):
    token = _get_token()
    if properties is None:
        properties = dict()

    if "token" not in properties:
        properties["token"] = token

    url = getattr(settings, 'APP_METRICS_MIXPANEL_API_URL', "http://api.mixpanel.com/track/")

    params = {"event": slug, "properties": properties}
    b64_data = base64.b64encode(json.dumps(params).encode('utf8'))

    data = urllib.parse.urlencode({"data": b64_data}).encode('utf8')
    req = urllib.request.Request(url, data)
    for i in range(num):
        response = urllib.request.urlopen(req)
        if response.read() == '0':
            raise MixPanelTrackError('MixPanel returned 0')


# Statsd tasks

def get_statsd_client():
    if statsd is None:
        raise ImproperlyConfigured("You must install 'python-statsd' in order to use this backend.")

    client = statsd.StatsClient(
        host=getattr(settings, 'APP_METRICS_STATSD_HOST', 'localhost'),
        port=int(getattr(settings, 'APP_METRICS_STATSD_PORT', 8125)),
    )
    return client


@task
def statsd_metric_task(slug, num=1, **kwargs):
    client = get_statsd_client()
    client.incr(slug, count=num, rate=float(getattr(settings, 'APP_METRICS_STATSD_SAMPLE_RATE', 1)))


@task
def statsd_timing_task(slug, seconds_taken=1.0, **kwargs):
    client = get_statsd_client()

    # You might be wondering "Why not use ``timer.start/.stop`` here?"
    # The problem is that this is a task, likely running out of process
    # & perhaps with network overhead. We'll measure the timing elsewhere,
    # in-process, to be as accurate as possible, then use the out-of-process
    # task for talking to the statsd backend.

    # Must convert to milliseconds
    # https://statsd.readthedocs.io/en/v3.3/timing.html#calling-timing-manually
    client.timing(slug, int(seconds_taken * 1000), rate=float(getattr(settings, 'APP_METRICS_STATSD_SAMPLE_RATE', 1)))


@task
def statsd_gauge_task(slug, current_value, **kwargs):
    client = get_statsd_client()
    if isinstance(current_value, str):
        current_value = Decimal(current_value)

    client.gauge(slug, current_value, rate=float(getattr(settings, 'APP_METRICS_STATSD_SAMPLE_RATE', 1)))


# Redis tasks

def get_redis_conn():
    if redis is None:
        raise ImproperlyConfigured("You must install 'redis' in order to use this backend.")
    conn = redis.StrictRedis(
        host=getattr(settings, 'APP_METRICS_REDIS_HOST', 'localhost'),
        port=getattr(settings, 'APP_METRICS_REDIS_PORT', 6379),
        db=getattr(settings, 'APP_METRICS_REDIS_DB', 0),
    )
    return conn


@task
def redis_metric_task(slug, num=1, **kwargs):
    # Record a metric in redis. We prefix our key here with 'm' for Metric
    # and build keys for each day, week, month, and year
    r = get_redis_conn()

    # Build keys
    now = datetime.datetime.now()
    day_key = "m:%s:%s" % (slug, now.strftime("%Y-%m-%d"))
    week_key = "m:%s:w:%s" % (slug, now.strftime("%U"))
    month_key = "m:%s:m:%s" % (slug, now.strftime("%Y-%m"))
    year_key = "m:%s:y:%s" % (slug, now.strftime("%Y"))

    # Increment keys
    r.incrby(day_key, num)
    r.incrby(week_key, num)
    r.incrby(month_key, num)
    r.incrby(year_key, num)


@task
def redis_gauge_task(slug, current_value, **kwargs):
    # We prefix our keys with a 'g' here for Gauge to avoid issues
    # of having a gauge and metric of the same name
    r = get_redis_conn()
    r.set("g:%s" % slug, current_value)

# Librato tasks

@task
def librato_metric_task(name, num, **kwargs):
    api = librato.connect(settings.APP_METRICS_LIBRATO_USER,
                          settings.APP_METRICS_LIBRATO_TOKEN)
    source = settings.APP_METRICS_LIBRATO_SOURCE
    api.submit(name, num, source=source, **kwargs)
