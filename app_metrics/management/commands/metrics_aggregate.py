import datetime 
from django.core.management.base import NoArgsCommand 

from app_metrics.models import Metric, MetricItem, MetricDay, MetricWeek, MetricMonth, MetricYear 

class Command(NoArgsCommand): 
    help = "Aggregate Application Metrics" 

    requires_model_validation = True 

    def handle_noargs(self, **options): 
        """ Aggregate Application Metrics """ 

        # Aggregate Item data into Days 
        items = MetricItem.objects.all() 

        for i in items: 
            day,create = MetricDay.objects.get_or_create(metric=i.metric, 
                                                         created=i.created)

            day.num = day.num + i.num
            day.save() 

        # Kill off our items 
        items.delete() 
