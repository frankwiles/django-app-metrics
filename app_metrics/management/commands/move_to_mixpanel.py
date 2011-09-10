from django.core.management.base import NoArgsCommand 

from app_metrics.models import MetricItem
from app_metrics.backends.mixpanel import metric

class Command(NoArgsCommand): 
    help = "Move MetricItems from the db backend to MixPanel" 

    requires_model_validation = True 

    def handle_noargs(self, **options): 
        """ Move MetricItems from the db backend to MixPanel" """ 

        backend = get_backend() 

        # If not using Mixpanel this command is a NOOP
        if backend != 'app_metrics.backends.mixpanel': 
            print "You need to set the backend to MixPanel"
            return 

        items = MetricItem.objects.all() 

        for i in items:
            properties = {
                'time': i.created.strftime('%s'),
            }
            metric(i.metric.slug, num=i.num, properties=properties)

        # Kill off our items 
        items.delete() 
