from django.contrib import admin 

from app_metrics.models import Metric, MetricSet, MetricItem, MetricDay, MetricWeek, MetricMonth, MetricYear 

class MetricAdmin(admin.ModelAdmin): 
    model = Metric 

admin.site.register(Metric, MetricAdmin)

class MetricInline(admin.StackedInline):
    model = Metric 
    extra = 1 

class MetricSetAdmin(admin.ModelAdmin): 
     model = MetricSet
     inlines = [MetricInline]

admin.site.register(MetricSet, MetricSetAdmin) 

class MetricDayAdmin(admin.ModelAdmin): 
    model = MetricDay 

admin.site.register(MetricDay, MetricDayAdmin) 

class MetricWeekAdmin(admin.ModelAdmin): 
    model = MetricWeek

admin.site.register(MetricWeek, MetricWeekAdmin) 

class MetricMonthAdmin(admin.ModelAdmin): 
    model = MetricMonth

admin.site.register(MetricMonth, MetricMonthAdmin) 

class MetricYearAdmin(admin.ModelAdmin): 
    model = MetricYear

admin.site.register(MetricYear, MetricYearAdmin) 


