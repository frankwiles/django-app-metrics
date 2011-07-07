# Backend to handle sending app metrics directly to mixpanel.com 
# See http://mixpanel.com/api/docs/ for more information on their API 

import base64
import json 
import urllib
import urllib2

from celery.decorators import task 

from django.conf import settings 
from django.core.exceptions import ImproperlyConfigured

def _get_token(): 
    token = getattr(settings, 'APP_METRICS_MIXPANEL_TOKEN', None) 

    if not token: 
        raise ImproperlyConfigured("You must define APP_METRICS_MIXPANEL_TOKEN when using the mixpanel backend.") 
    else: 
        return token 

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
    for i in range(num):
        req = urllib2.Request(url, data) 
        response = urllib2.urlopen(req) 


