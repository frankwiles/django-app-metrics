from django.conf.urls import patterns, url
from app_metrics.views import MonthlyMetricReport, YearlyMetricReport, MetricReports

# Add these URLs to your main urlconf. Be sure to keep the namespace and app_name as `app_metrics`, the templates explicitly use them
# e.g.
#   (r'^metrics/', include('app_metrics.urls', namespace='app_metrics', app_name='app_metrics')),


urlpatterns = patterns('',
    url(r'^report/yearly/(?P<year>\d{4})/$', YearlyMetricReport.as_view(), name="yearly_metric_report"),
    url(r'^report/monthly/(?P<month>\w{3})/(?P<year>\d{4})/$', MonthlyMetricReport.as_view(), name="monthly_metric_report"),
    url(r'^reports/$', MetricReports.as_view(), name="metric_reports"),
)
