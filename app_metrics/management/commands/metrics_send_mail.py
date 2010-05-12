from django.core.management.base import NoArgsCommand 

class Command(NoArgsCommand): 
    help = "Aggregate Application Metrics" 

    requires_model_validation = True 

    def handle_noargs(self, **options): 
        """ Aggregate Application Metrics """ 
        pass 

