# Backend to handle sending app metrics directly to mixpanel.com
# See http://mixpanel.com/api/docs/ for more information on their API

from django.conf import settings
from app_metrics.tasks import mixpanel_metric_task
from app_metrics.tasks import _get_token


def metric(slug, num=1, properties=None):
    """
    Send metric directly to Mixpanel

    - slug here will be used as the Mixpanel "event" string
    - if num > 1, we will loop over this and send multiple
    - properties are a dictionary of additional information you
      may want to pass to Mixpanel.  For example you might use it like:

      metric("invite-friends",
             properties={"method": "email", "number-friends": "12", "ip": "123.123.123.123"})
    """
    token = _get_token()
    mixpanel_metric_task.delay(slug, num, properties)


def timing(slug, seconds_taken, **kwargs):
    # Unsupported, hence the noop.
    pass
