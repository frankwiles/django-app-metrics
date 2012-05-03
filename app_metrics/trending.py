import datetime

from django.core.exceptions import ObjectDoesNotExist

from app_metrics.models import Metric, MetricItem, MetricDay, MetricWeek, MetricMonth, MetricYear
from app_metrics.utils import week_for_date, month_for_date, year_for_date, get_previous_month, get_previous_year

class InvalidMetric(Exception): pass

def trending_for_metric(metric=None, date=None):
    """ Build a dictionary of trending values for a given metric """

    if not isinstance(metric, Metric):
        raise InvalidMetric('No Metric instance passed to trending_for_metric()')
    if not date:
        date = datetime.date.today()

    data = {}

    # Get current day values so far
    if date == datetime.date.today():
        data['current_day'] = _trending_for_current_day(metric)

    data['yesterday']   = _trending_for_yesterday(metric)
    data['week']        = _trending_for_week(metric)
    data['month']       = _trending_for_month(metric)
    data['year']        = _trending_for_year(metric)

    return data

def _trending_for_current_day(metric=None):
    date = datetime.date.today()
    unaggregated_values = MetricItem.objects.filter(metric=metric)
    aggregated_values = MetricDay.objects.filter(metric=metric, created=date)
    count = 0

    for u in unaggregated_values:
        count = count + u.num

    for a in aggregated_values:
        count = count + a.num

    return count

def _trending_for_yesterday(metric=None):
    today = datetime.date.today()
    yesterday_date = today - datetime.timedelta(days=1)
    previous_week_date = today - datetime.timedelta(weeks=1)
    previous_month_date = get_previous_month(today)

    data = {
            'yesterday': 0,
            'previous_week': 0,
            'previous_month': 0,
    }

    try:
        yesterday = MetricDay.objects.get(metric=metric, created=yesterday_date)
        data['yesterday'] = yesterday.num
    except ObjectDoesNotExist:
        pass

    try: 
        previous_week = MetricDay.objects.get(metric=metric, created=previous_week_date)
        data['previous_week'] = previous_week.num
    except ObjectDoesNotExist:
        pass

    try:
        previous_month = MetricDay.objects.get(metric=metric, created=previous_month_date)
        data['previous_month'] = previous_month.num
    except ObjectDoesNotExist:
        pass

    return data

def _trending_for_week(metric=None):
    this_week_date = week_for_date(datetime.date.today())
    previous_week_date = this_week_date - datetime.timedelta(weeks=1)
    previous_month_week_date = get_previous_month(this_week_date)
    previous_year_week_date = get_previous_year(this_week_date)

    data = {
            'week': 0,
            'previous_week': 0,
            'previous_month_week': 0,
            'previous_year_week': 0,
    }

    try:
        week = MetricWeek.objects.get(metric=metric, created=this_week_date)
        data['week'] = week.num
    except ObjectDoesNotExist:
        pass

    try:
        previous_week = MetricWeek.objects.get(metric=metric, created=previous_week_date)
        data['previous_week'] = previous_week.num
    except ObjectDoesNotExist:
        pass

    try:
        previous_month_week = MetricWeek.objects.get(metric=metric, created=previous_month_week_date)
        data['previous_month_week'] = previous_month_week.num
    except ObjectDoesNotExist:
        pass

    try:
        previous_year_week = MetricWeek.objects.get(metric=metric, created=previous_year_week_date)
        data['previous_year_week'] = previous_year_week.num
    except ObjectDoesNotExist:
        pass

    return data

def _trending_for_month(metric=None):
    this_month_date = month_for_date(datetime.date.today())
    previous_month_date = get_previous_month(this_month_date)
    previous_month_year_date = get_previous_year(this_month_date)

    data = {
            'month': 0,
            'previous_month': 0,
            'previous_month_year': 0
    }

    try:
        month = MetricMonth.objects.get(metric=metric, created=this_month_date)
        data['month'] = month.num
    except ObjectDoesNotExist:
        pass

    try:
        previous_month = MetricMonth.objects.get(metric=metric, created=previous_month_date)
        data['previous_month'] = previous_month.num
    except ObjectDoesNotExist:
        pass

    try:
        previous_month_year = MetricMonth.objects.get(metric=metric, created=previous_month_year_date)
        data['previous_month_year'] = previous_month_year.num
    except ObjectDoesNotExist:
        pass

    return data

def _trending_for_year(metric=None):
    this_year_date = year_for_date(datetime.date.today())
    previous_year_date = get_previous_year(this_year_date)

    data = {
            'year': 0,
            'previous_year': 0,
    }

    try:
        year = MetricYear.objects.get(metric=metric, created=this_year_date)
        data['year'] = year.num
    except ObjectDoesNotExist:
        pass

    try:
        previous_year = MetricYear.objects.get(metric=metric, created=previous_year_date)
        data['previous_year'] = previous_year.num
    except ObjectDoesNotExist:
        pass

    return data
