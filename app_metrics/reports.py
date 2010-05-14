import datetime 

from django.template.loader import render_to_string 

from app_metrics.models import * 
from app_metrics.trending import trending_for_metric 

def generate_report(metric_set=None, html=False): 
    """ Generate a Metric Set Report """ 

    # Get trending data for each metric 
    metric_trends = []
    for m in metric_set.metrics.all(): 
        data = {'metric': m}
        data['trends'] = trending_for_metric(m)
        metric_trends.append(data)
   
    message = render_to_string('app_metrics/email.txt', { 
                            'metric_set': metric_set, 
                            'metrics': metric_trends, 
                            'today': datetime.date.today(),
                })

    if html: 
        message_html = render_to_string('app_metrics/email.html', { 
                            'metric_set': metric_set, 
                            'metrics': metric_trends, 
                            'today': datetime.date.today(),
                })

        return message, message_html 

    else: 
        return message 
