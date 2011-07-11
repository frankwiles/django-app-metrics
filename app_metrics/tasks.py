import base64
import json 
import urllib
import urllib2

from django.conf import settings 
from celery.decorators import task 
from app_metrics.backend.mixpanel import _get_token

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
