from decimal import Decimal
from unittest import mock
import time
from django.test import TestCase
from django.conf import settings
from app_metrics.utils import metric, timing, gauge
from unittest import skipUnless

try:
    import statsd
except ImportError:
    statsd = None


@skipUnless(statsd, "No statsd module. Skipping.")
class StatsdCreationTests(TestCase):
    def setUp(self):
        super(StatsdCreationTests, self).setUp()
        self.old_backend = getattr(settings, 'APP_METRICS_BACKEND', None)
        settings.APP_METRICS_BACKEND = 'app_metrics.backends.statsd'

    def test_metric(self):
        with mock.patch('statsd.StatsClient._send') as mock_client_send:
            mock_client_send.return_value = 1

            metric('testing')
            mock_client_send.assert_called_with('testing:1|c')

            metric('testing', 2)
            mock_client_send.assert_called_with('testing:2|c')

            metric('another', 4)
            mock_client_send.assert_called_with('another:4|c')

    def test_timing(self):
        with mock.patch('statsd.StatsClient._send') as mock_client_send:
            mock_client_send.return_value = 1

            with timing('testing'):
                time.sleep(0.025)

            args, kwargs = mock_client_send.call_args
            self.assertRegex(args[0], r'testing:\d{2}\.0000|ms')

    def test_gauge(self):
        with mock.patch('statsd.StatsClient._send') as mock_client_send:
            mock_client_send.return_value = 1

            gauge('testing', 10.5)
            mock_client_send.assert_called_with('testing:10.5|g')

            gauge('testing', Decimal('6.576'))
            mock_client_send.assert_called_with('testing:6.576|g')

            gauge('another', 1)
            mock_client_send.assert_called_with('another:1|g')

    def tearDown(self):
        settings.APP_METRICS_BACKEND = self.old_backend
        super(StatsdCreationTests, self).tearDown()
