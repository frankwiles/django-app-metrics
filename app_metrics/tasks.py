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
