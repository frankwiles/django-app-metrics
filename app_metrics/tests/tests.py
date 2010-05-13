from django.test import TestCase 

from django.core import management 
from django.contrib.auth.models import User 
from django.conf import settings 

from app_metrics.models import Metric, MetricItem, MetricDay, MetricWeek, MetricMonth, MetricYear
from app_metrics.utils import metric, create_metric  

class MetricCreationTests(TestCase): 
   
    def setUp(self): 
        self.user1 = User.objects.create_user('user1', 'user1@example.com', 'user1pass')
        self.user2 = User.objects.create_user('user2', 'user2@example.com', 'user2pass')

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

class MetricAggregationTests(TestCase): 

    def setUp(self): 
        self.user1 = User.objects.create_user('user1', 'user1@example.com', 'user1pass')
        self.user2 = User.objects.create_user('user2', 'user2@example.com', 'user2pass')
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
    pass 

class EmailTests(TestCase): 
    """ Test that our emails send properly """ 
    pass 

