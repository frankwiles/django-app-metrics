import datetime 

from django.core.management.base import NoArgsCommand 
from django.conf import settings 

from app_metrics.reports import generate_report

from app_metrics.models import MetricSet, Metric 

class Command(NoArgsCommand): 
    help = "Send Report E-mails" 

    requires_model_validation = True 

    def handle_noargs(self, **options): 
        """ Send Report E-mails """ 

        # Determine if we should also send any weekly or monthly reports 
        today = datetime.date.today() 
        if today.weekday == 0: 
            send_weekly = True
        else: 
            send_weekly = False 

        if today.day == 1: 
            send_monthly = True 
        else: 
            send_monthly = False 

        qs = MetricSet.objects.filter(send_daily=True, no_email=False, send_monthly=send_monthly, send_weekly=send_weekly)

        if "mailer" in settings.INSTALLED_APPS: 
            from mailer import send_html_mail 
            SEND_HTML = True 
        else: 
            from django.core.mail import send_mail 
            SEND_HTML = False 

        for s in qs: 
            subject = "%s Report" % s.name 

            if SEND_HTML: 
                (message, message_html) = generate_report(s, html=True)
                send_html_mail(subject=subject, 
                               message=message, 
                               message_html=message_html, 
                               from_email=settings.DEFAULT_FROM_EMAIL, 
                               recipient_list=s.email_recipients.all())
            else: 
                message = generate_report(s)
                send_mail(subject=subject,
                          message=message, 
                          from_email=settings.DEFAULT_FROM_EMAIL, 
                          recipient_list=s.email_recipients.all())

