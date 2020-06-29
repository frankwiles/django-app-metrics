from django.conf.urls import url

from app_metrics.views import metric_report_view


urlpatterns = [
    url(r'^reports/$',
        metric_report_view,
        name='app_metrics_reports',
       ),
]
