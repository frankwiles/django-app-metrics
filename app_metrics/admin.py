from django.contrib import admin

from app_metrics.models import (Metric, MetricSet, MetricItem, MetricDay,
                                MetricWeek, MetricMonth, MetricYear, Threshold, DayChoiceField
                                )

from bitfield.forms import BitFieldCheckboxSelectMultiple


class ThresholdAdmin(admin.ModelAdmin):
    list_display = ('describe', 'active')
    list_filter = ['metric__name']
    formfield_overrides = {
        DayChoiceField: {'widget': BitFieldCheckboxSelectMultiple},
    }

class MetricAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'slug', 'num')
    list_filter = ['metric__name']

    def slug(self, obj):
        return obj.metric.slug

admin.site.register(Metric)
admin.site.register(MetricSet)
admin.site.register(Threshold, ThresholdAdmin)
admin.site.register(MetricDay, MetricAdmin)
admin.site.register(MetricWeek, MetricAdmin)
admin.site.register(MetricMonth, MetricAdmin)
admin.site.register(MetricYear, MetricAdmin)
admin.site.register(MetricItem, MetricAdmin)
