import mock
from django.test import TestCase
from django.conf import settings
from app_metrics.utils import metric, gauge

class RedisTests(TestCase):
    def setUp(self):
        super(RedisTests, self).setUp()
        self.old_backend = getattr(settings, 'APP_METRICS_BACKEND', None)
        settings.APP_METRICS_BACKEND = 'app_metrics.backends.redis'

    def tearDown(self):
        settings.APP_METRICS_BACKEND = self.old_backend
        super(RedisTests, self).tearDown()

    def test_metric(self):
        with mock.patch('redis.client.StrictRedis') as mock_client:
            instance = mock_client.return_value
            instance._send.return_value = 1

            metric('foo')
            mock_client._send.asert_called_with(mock.ANY, {'slug':'foo', 'num':'1'})

    def test_gauge(self):
        with mock.patch('redis.client.StrictRedis') as mock_client:
            instance = mock_client.return_value
            instance._send.return_value = 1

            gauge('testing', 10.5)
            mock_client._send.asert_called_with(mock.ANY, {'slug':'testing', 'current_value':'10.5'})

