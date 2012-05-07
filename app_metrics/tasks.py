import base64
import json
import urllib
import urllib2

try:
    from celery.task import task
except ImportError:
    from celery.decorators import task

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from app_metrics.models import Metric, MetricItem

try:
    # Not required. If we do this once at the top of the module, we save
    # ourselves the pain of importing every time the task fires.
    import statsd
except ImportError:
    statsd = None


class MixPanelTrackError(Exception):
    pass


@task
def db_metric_task(slug, num=1, **kwargs):
    met = Metric.objects.get(slug=slug)
    MetricItem.objects.create(metric=met, num=num)


def _get_token():
    token = getattr(settings, 'APP_METRICS_MIXPANEL_TOKEN', None)

    if not token:
        raise ImproperlyConfigured("You must define APP_METRICS_MIXPANEL_TOKEN when using the mixpanel backend.")
    else:
        return token


@task
def mixpanel_metric_task(slug, num, properties=None, **kwargs):

    token = _get_token()
    if properties == None:
        properties = dict()

    if "token" not in properties:
        properties["token"] = token

    url = getattr(settings, 'APP_METRICS_MIXPANEL_API_URL', "http://api.mixpanel.com/track/")

    params = {"event": slug, "properties": properties}
    b64_data = base64.b64encode(json.dumps(params))

    data = urllib.urlencode({"data": b64_data})
    req = urllib2.Request(url, data)
    for i in range(num):
        response = urllib2.urlopen(req)
        if response.read() == '0':
            raise MixPanelTrackError(u'MixPanel returned 0')


@task
def statsd_metric_task(slug, num=1, **kwargs):
    if statsd is None:
        raise ImproperlyConfigured("You must install 'python-statsd' in order to use this backend.")

    conn = statsd.Connection(
        host=getattr(settings, 'APP_METRICS_STATSD_HOST', 'localhost'),
        port=int(getattr(settings, 'APP_METRICS_STATSD_PORT', 8125)),
        sample_rate=float(getattr(settings, 'APP_METRICS_STATSD_SAMPLE_RATE', 1)),
    )

    counter = statsd.Counter(slug, connection=conn)
    counter += num


@task
def statsd_timing_task(slug, seconds_taken=1.0, **kwargs):
    if statsd is None:
        raise ImproperlyConfigured("You must install 'python-statsd' in order to use this backend.")

    conn = statsd.Connection(
        host=getattr(settings, 'APP_METRICS_STATSD_HOST', 'localhost'),
        port=int(getattr(settings, 'APP_METRICS_STATSD_PORT', 8125)),
        sample_rate=float(getattr(settings, 'APP_METRICS_STATSD_SAMPLE_RATE', 1)),
    )

    # You might be wondering "Why not use ``timer.start/.stop`` here?"
    # The problem is that this is a task, likely running out of process
    # & perhaps with network overhead. We'll measure the timing elsewhere,
    # in-process, to be as accurate as possible, then use the out-of-process
    # task for talking to the statsd backend.
    timer = statsd.Timer(slug, connection=conn)
    timer.send('total', seconds_taken)
