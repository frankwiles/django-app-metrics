from django.core.management.base import NoArgsCommand 
from app_metrics.models import Threshold
from app_metrics.utils import get_backend 

class Command(NoArgsCommand): 
    help = "Run Metric Thresholds" 

    requires_model_validation = True 

    def handle_noargs(self, **options): 
        backend = get_backend() 
        # If using Mixpanel this command is a NOOP
        if backend == 'app_metrics.backends.mixpanel': 
            print "Useless use of run_thresholds when using Mixpanel backend"
            return 

        [ t.test() for t in Threshold.active.all() ]
