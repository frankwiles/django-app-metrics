import datetime 
from django.core.management.base import NoArgsCommand 

from app_metrics.models import Metric, MetricItem, MetricDay, MetricWeek, MetricMonth, MetricYear 

class Command(NoArgsCommand): 
    help = "Aggregate Application Metrics" 

    requires_model_validation = True 

    def _week_for_date(self, date=None): 
        return date - datetime.timedelta(days=date.weekday())

    def _month_for_date(self, month=None): 
        return month - datetime.timedelta(days=month.day-1)

    def _year_for_date(self, year=None): 
        return datetime.date(year.year, 01, 01)

    def handle_noargs(self, **options): 
        """ Aggregate Application Metrics """ 

        # Aggregate Items
        items = MetricItem.objects.all() 

        for i in items: 
            # Daily Aggregation 
            day,create = MetricDay.objects.get_or_create(metric=i.metric, 
                                                         created=i.created)

            day.num = day.num + i.num
            day.save() 

            # Weekly Aggregation 
            week_date = self._week_for_date(i.created)
            week, create = MetricWeek.objects.get_or_create(metric=i.metric,
                                                            created=week_date)

            week.num = week.num + i.num 
            week.save() 

            # Monthly Aggregation 
            month_date = self._month_for_date(i.created) 
            month, create = MetricMonth.objects.get_or_create(metric=i.metric,
                                                              created=month_date)
            month.num = month.num + i.num 
            month.save() 

            # Yearly Aggregation 
            year_date = self._year_for_date(i.created) 
            year, create = MetricYear.objects.get_or_create(metric=i.metric,
                                                              created=year_date)
            year.num = year.num + i.num 
            year.save() 

        # Kill off our items 
        items.delete() 
