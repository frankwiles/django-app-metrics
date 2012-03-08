from django.test import TestCase 
from django.conf import settings 
from django.core.exceptions import ImproperlyConfigured 

from app_metrics.utils import * 

class MixpanelMetricConfigTests(TestCase): 

    def setUp(self): 
        self.old_backend = settings.APP_METRICS_BACKEND
        settings.APP_METRICS_BACKEND = 'app_metrics.backends.mixpanel'

    def test_metric(self): 
        self.assertRaises(ImproperlyConfigured, metric, 'test_metric')

    def tearDown(self): 
        settings.APP_METRICS_BACKEND = self.old_backend 

class MixpanelCreationTests(TestCase): 

    def setUp(self): 
        self.old_backend = settings.APP_METRICS_BACKEND
        self.old_token = settings.APP_METRICS_MIXPANEL_TOKEN 
        settings.APP_METRICS_BACKEND = 'app_metrics.backends.mixpanel'
        settings.APP_METRICS_MIXPANEL_TOKEN = 'foobar'

    def test_metric(self): 
        metric('testing') 

    def tearDown(self): 
        settings.APP_METRICS_BACKEND = self.old_backend 
        settings.APP_METRICS_MIXPANEL_TOKEN = self.old_token 
