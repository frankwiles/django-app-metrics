import mock
from django.test import TestCase
from django.conf import settings
from app_metrics.utils import metric


class StatsdCreationTests(TestCase):
    def setUp(self):
        super(StatsdCreationTests, self).setUp()
        self.old_backend = getattr(settings, 'APP_METRICS_BACKEND', None)
        settings.APP_METRICS_BACKEND = 'app_metrics.backends.statsd'

    def test_metric(self):
        with mock.patch('statsd.Client') as mock_client:
            instance = mock_client.return_value
            instance._send.return_value = 1

            metric('testing')
            mock_client._send.assert_called_with(mock.ANY, {'testing': '1|c'})

            metric('testing', 2)
            mock_client._send.assert_called_with(mock.ANY, {'testing': '2|c'})

            metric('another', 4)
            mock_client._send.assert_called_with(mock.ANY, {'another': '4|c'})

    def tearDown(self):
        settings.APP_METRICS_BACKEND = self.old_backend
        super(StatsdCreationTests, self).tearDown()
