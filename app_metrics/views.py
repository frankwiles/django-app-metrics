
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response 
from django.template import RequestContext 

@login_required 
def metric_report_view(request):
    return render_to_response('app_metrics/reports.html', {}, context_instance=RequestContext(request))



