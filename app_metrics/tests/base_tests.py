import datetime
from decimal import Decimal
import mock

from django.test import TestCase
from django.core import management
from django.conf import settings
from django.core import mail
from django.contrib.auth.models import User

from app_metrics.exceptions import TimerError
from app_metrics.models import Metric, MetricItem, MetricDay, MetricWeek, MetricMonth, MetricYear, Gauge
from app_metrics.utils import *
from app_metrics.trending import _trending_for_current_day, _trending_for_yesterday, _trending_for_week, _trending_for_month, _trending_for_year

class MetricCreationTests(TestCase):

    def test_metric(self):
        new_metric = create_metric(name='Test Metric Class',
                                   slug='test_metric')

        metric('test_metric')
        metric('test_metric')
        metric('test_metric')

        current_count = MetricItem.objects.filter(metric=new_metric)

        self.assertEqual(len(current_count), 3)
        self.assertEqual(current_count[0].num, 1)
        self.assertEqual(current_count[1].num, 1)
        self.assertEqual(current_count[2].num, 1)

    def test_get_or_create_metric(self):
        new_metric = get_or_create_metric(name='Test Metric Class',
                                          slug='test_metric')

        metric('test_metric')
        metric('test_metric')
        metric('test_metric')

        new_metric = get_or_create_metric(name='Test Metric Class',
                                          slug='test_metric')

        current_count = MetricItem.objects.filter(metric=new_metric)
        self.assertEqual(len(current_count), 3)
        self.assertEqual(current_count[0].num, 1)
        self.assertEqual(current_count[1].num, 1)
        self.assertEqual(current_count[2].num, 1)

class MetricAggregationTests(TestCase):

    def setUp(self):
        self.metric1 = create_metric(name='Test Aggregation1', slug='test_agg1')
        self.metric2 = create_metric(name='Test Aggregation2', slug='test_agg2')

        metric('test_agg1')
        metric('test_agg1')

        metric('test_agg2')
        metric('test_agg2')
        metric('test_agg2')

    def test_daily_aggregation(self):
        management.call_command('metrics_aggregate')

        day1 = MetricDay.objects.get(metric=self.metric1)
        day2 = MetricDay.objects.get(metric=self.metric2)
        self.assertEqual(day1.num, 2)
        self.assertEqual(day2.num, 3)

    def test_weekly_aggregation(self):
        management.call_command('metrics_aggregate')

        week1 = MetricWeek.objects.get(metric=self.metric1)
        week2 = MetricWeek.objects.get(metric=self.metric2)
        self.assertEqual(week1.num, 2)
        self.assertEqual(week2.num, 3)

    def test_monthly_aggregation(self):
        management.call_command('metrics_aggregate')

        month1 = MetricMonth.objects.get(metric=self.metric1)
        month2 = MetricMonth.objects.get(metric=self.metric2)
        self.assertEqual(month1.num, 2)
        self.assertEqual(month2.num, 3)

    def test_yearly_aggregation(self):
        management.call_command('metrics_aggregate')

        year1 = MetricYear.objects.get(metric=self.metric1)
        year2 = MetricYear.objects.get(metric=self.metric2)
        self.assertEqual(year1.num, 2)
        self.assertEqual(year2.num, 3)

class TrendingTests(TestCase):
    """ Test that our trending logic works """

    def setUp(self):
        #self.user1 = User.objects.create_user('user1', 'user1@example.com', 'user1pass')
        #self.user2 = User.objects.create_user('user2', 'user2@example.com', 'user2pass')
        self.metric1 = create_metric(name='Test Trending1', slug='test_trend1')
        self.metric2 = create_metric(name='Test Trending2', slug='test_trend2')

    def test_trending_for_current_day(self):
        """ Test current day trending counter """
        metric('test_trend1')
        metric('test_trend1')
        management.call_command('metrics_aggregate')
        metric('test_trend1')
        metric('test_trend1')

        count = _trending_for_current_day(self.metric1)
        self.assertEqual(count,4)

    def test_trending_for_yesterday(self):
        """ Test yesterday trending """
        today = datetime.date.today()
        yesterday_date = today - datetime.timedelta(days=1)
        previous_week_date = today - datetime.timedelta(weeks=1)
        previous_month_date = get_previous_month(today)

        MetricDay.objects.create(metric=self.metric1, num=5, created=yesterday_date)
        MetricDay.objects.create(metric=self.metric1, num=4, created=previous_week_date)
        MetricDay.objects.create(metric=self.metric1, num=3, created=previous_month_date)

        data = _trending_for_yesterday(self.metric1)
        self.assertEqual(data['yesterday'], 5)
        self.assertEqual(data['previous_week'], 4)
        self.assertEqual(data['previous_month'], 3)

    def test_trending_for_week(self):
        """ Test weekly trending data """
        this_week_date = week_for_date(datetime.date.today())
        previous_week_date = this_week_date - datetime.timedelta(weeks=1)
        previous_month_date = get_previous_month(this_week_date)
        previous_year_date = get_previous_year(this_week_date)

        MetricWeek.objects.create(metric=self.metric1, num=5, created=this_week_date)
        MetricWeek.objects.create(metric=self.metric1, num=4, created=previous_week_date)
        MetricWeek.objects.create(metric=self.metric1, num=3, created=previous_month_date)
        MetricWeek.objects.create(metric=self.metric1, num=2, created=previous_year_date)

        data = _trending_for_week(self.metric1)
        self.assertEqual(data['week'],5)
        self.assertEqual(data['previous_week'],4)
        self.assertEqual(data['previous_month_week'],3)
        self.assertEqual(data['previous_year_week'],2)

    def test_trending_for_month(self):
        """ Test monthly trending data """
        this_month_date = month_for_date(datetime.date.today())
        previous_month_date = get_previous_month(this_month_date)
        previous_month_year_date = get_previous_year(this_month_date)

        MetricMonth.objects.create(metric=self.metric1, num=5, created=this_month_date)
        MetricMonth.objects.create(metric=self.metric1, num=4, created=previous_month_date)
        MetricMonth.objects.create(metric=self.metric1, num=3, created=previous_month_year_date)

        data = _trending_for_month(self.metric1)
        self.assertEqual(data['month'],5)
        self.assertEqual(data['previous_month'],4)
        self.assertEqual(data['previous_month_year'],3)

    def test_trending_for_year(self):
        """ Test yearly trending data """
        this_year_date = year_for_date(datetime.date.today())
        previous_year_date = get_previous_year(this_year_date)

        MetricYear.objects.create(metric=self.metric1, num=5, created=this_year_date)
        MetricYear.objects.create(metric=self.metric1, num=4, created=previous_year_date)

        data = _trending_for_year(self.metric1)
        self.assertEqual(data['year'],5)
        self.assertEqual(data['previous_year'],4)

    def test_missing_trending(self):
        this_week_date = week_for_date(datetime.date.today())
        previous_week_date = this_week_date - datetime.timedelta(weeks=1)
        previous_month_date = get_previous_month(this_week_date)
        previous_year_date = get_previous_year(this_week_date)

        MetricWeek.objects.create(metric=self.metric1, num=5, created=this_week_date)
        MetricWeek.objects.create(metric=self.metric1, num=4, created=previous_week_date)
        MetricWeek.objects.create(metric=self.metric1, num=3, created=previous_month_date)

        data = _trending_for_week(self.metric1)
        self.assertEqual(data['week'],5)
        self.assertEqual(data['previous_week'],4)
        self.assertEqual(data['previous_month_week'],3)
        self.assertEqual(data['previous_year_week'],0)

class EmailTests(TestCase):
    """ Test that our emails send properly """
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@example.com', 'user1pass')
        self.user2 = User.objects.create_user('user2', 'user2@example.com', 'user2pass')
        self.metric1 = create_metric(name='Test Trending1', slug='test_trend1')
        self.metric2 = create_metric(name='Test Trending2', slug='test_trend2')
        self.set = create_metric_set(name="Fake Report",
                                     metrics=[self.metric1, self.metric2],
                                     email_recipients=[self.user1, self.user2])

    def test_email(self):
        """ Test email sending """
        metric('test_trend1')
        metric('test_trend1')
        metric('test_trend1')
        metric('test_trend2')
        metric('test_trend2')

        management.call_command('metrics_aggregate')
        management.call_command('metrics_send_mail')

        self.assertEqual(len(mail.outbox), 1)


class GaugeTests(TestCase):
    def setUp(self):
        self.gauge = Gauge.objects.create(
            name='Testing',
        )

    def test_existing_gauge(self):
        self.assertEqual(Gauge.objects.all().count(), 1)
        self.assertEqual(Gauge.objects.get(slug='testing').current_value, Decimal('0.00'))

        gauge('testing', '10.5')
        # We should not have created a new gauge
        self.assertEqual(Gauge.objects.all().count(), 1)
        self.assertEqual(Gauge.objects.get(slug='testing').current_value, Decimal('10.5'))

    def test_new_gauge(self):
        gauge('test_trend1', Decimal('12.373'))
        self.assertEqual(Gauge.objects.all().count(), 2)
        self.assertTrue('test_trend1' in list(Gauge.objects.all().values_list('slug', flat=True)))
        self.assertEqual(Gauge.objects.get(slug='test_trend1').current_value, Decimal('12.373'))


class TimerTests(TestCase):
    def setUp(self):
        super(TimerTests, self).setUp()
        self.timer = Timer()

    def test_start(self):
        with mock.patch('time.time') as mock_time:
            mock_time.return_value = '12345.0'
            self.timer.start()

        self.assertEqual(self.timer._start, '12345.0')

        self.assertRaises(TimerError, self.timer.start)

    def test_stop(self):
        self.assertRaises(TimerError, self.timer.stop)

        with mock.patch('time.time') as mock_time:
            mock_time.return_value = 12345.0
            self.timer.start()

        with mock.patch('time.time') as mock_time:
            mock_time.return_value = 12347.2
            self.timer.stop()

        self.assertAlmostEqual(self.timer._elapsed, 2.2)
        self.assertEqual(self.timer._start, None)

    def test_elapsed(self):
        self.assertRaises(TimerError, self.timer.elapsed)

        self.timer._elapsed = 2.2
        self.assertEqual(self.timer.elapsed(), 2.2)

    # The ``Timer.store()`` is tested as part of the statsd backend tests.
