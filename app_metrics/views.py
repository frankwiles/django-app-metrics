from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic.dates import  MonthArchiveView, YearArchiveView
from django.views.generic.base import TemplateView
from collections import defaultdict
from operator import attrgetter
from app_metrics.models import MetricDay, MetricMonth
from dateutil.rrule import MONTHLY, DAILY, rrule
import datetime, calendar


class BaseReport(object):

    @method_decorator(staff_member_required)  # all instance methods that inherit from this class will be admin required
    def dispatch(self, *args, **kwargs):
        return super(BaseReport, self).dispatch(*args, **kwargs)


class MetricReports(BaseReport, TemplateView):
    template_name = 'app_metrics/metric_reports.html'

    def get_context_data(self, **kwargs):
        """
        Grab all the unique dates for metric data that we have
        """
        return { 'title': 'Metric Reports', 'dates': MetricMonth.objects.all().dates('created', 'month', 'ASC') }


class BaseMetricReport(BaseReport):
    # django generic view needs these members
    template_name = 'app_metrics/metric_report.html'
    date_field = 'created'
    date_header_fields = 'date_headers'
    make_object_list = True
    context_object_name = 'metrics'
    
    @staticmethod
    def create_date_range(range_type, start_date, end_date):
        return rrule(range_type, dtstart=start_date, until=end_date)

    def create_date_list(self, date_list):
        """
        Should be overriden by children to create an appropriate date list
        """
        raise NotImplemented()

    def get_context_data(self, *args, **kwargs):
        """
        Re-organizing the metrics data and filling in the holes for days in which there is no data
        """
        context = super(BaseMetricReport, self).get_context_data(*args, **kwargs)
        context['title'] = getattr(self, 'title')
        metrics = defaultdict(dict)
        context['date_list'].sort()  # sort the django provided dates
        context['date_list'] = self.create_date_list(context['date_list'])
        # fill in the entries we have
        for entry in context.get(BaseMetricReport.context_object_name):
            metrics[entry.metric][getattr(entry.created, self.date_grouping_attr)] = entry
        # fill the holes for days we have no entries
        for metric in metrics.keys():
            for _date in context['date_list']:  # going through all the dates
                if metrics[metric].get(getattr(_date, self.date_grouping_attr), None) is None:  # fill in empty ones
                    # setting the correct created day so it sorts accordingly
                    date_args = {'year': _date.year, 'month': _date.month, 'day': _date.day}
                    date_args[self.date_grouping_attr] = getattr(_date, self.date_grouping_attr)
                    date_args = (date_args.get('year'), date_args.get('month'), date_args.get('day'))
                    metrics[metric][getattr(_date, self.date_grouping_attr)] = self.klass(num=0, metric=metric, created=datetime.date(*date_args)) # sticking an unsaved item with 0 as a placeholder
        # format our date list
        context['date_list'] = [ d.strftime(getattr(self, 'format_string')) for d in context['date_list'] ]
        # sort metric entries are by date as well
        for m in metrics.keys():  
            metrics[m] = metrics[m].values()  # flatten this dict out
            metrics[m].sort(key=attrgetter('created'))
        context[BaseMetricReport.context_object_name] = metrics.items() # calling items here to make the template cleaner/template didnt like calling items in there
        return context


class MonthlyMetricReport(BaseMetricReport, MonthArchiveView):
    queryset = MetricDay.objects.all()  # django generic view expects this
    # below members are used internally
    klass = MetricDay  
    format_string = "%m/%d"
    title = 'Monthly Metric Report'
    date_grouping_attr = 'day'

    def create_date_list(self, date_list):
        """
        Creates a list of date objects that represent each day of the month for a given month
        """
        found_day = date_list[0]
        _, last_day_of_month = calendar.monthrange(found_day.year, found_day.month)
        return list(BaseMetricReport.create_date_range(DAILY, datetime.date(found_day.year, found_day.month, 1), datetime.date(found_day.year, found_day.month, last_day_of_month)))


class YearlyMetricReport(BaseMetricReport, YearArchiveView):
    klass = MetricMonth
    queryset = MetricMonth.objects.all()
    format_string = "%B"
    title = 'Yearly Metric Report'
    date_grouping_attr = 'month'

    def create_date_list(self, date_list):
        """
        Creates a list of date objects that represent each month of the year for a given year
        """
        found_day = date_list[0]
        return list(BaseMetricReport.create_date_range(MONTHLY, datetime.date(found_day.year, 1, 1), datetime.date(found_day.year, 12, 1)))
