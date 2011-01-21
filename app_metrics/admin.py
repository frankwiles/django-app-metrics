from django.contrib import admin 

from app_metrics.models import Metric, MetricSet, MetricItem, MetricDay, MetricWeek, MetricMonth, MetricYear

admin.site.register(Metric)
admin.site.register(MetricSet)
admin.site.register(MetricDay)
admin.site.register(MetricWeek)
admin.site.register(MetricMonth)
admin.site.register(MetricYear) 
admin.site.register(MetricItem) 
