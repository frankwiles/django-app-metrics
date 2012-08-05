import datetime 
import string

from django.core.management.base import NoArgsCommand 
from django.conf import settings 
from django.db.models import Q
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from app_metrics.reports import generate_report
from app_metrics.models import MetricSet, Metric 
from app_metrics.utils import get_backend 

class Command(NoArgsCommand): 
    help = "Send Report E-mails" 
    requires_model_validation = True 
    can_import_settings = True 

    def handle_noargs(self, **options): 
        """ Send Report E-mails """ 

        from django.conf import settings
        translation.activate(settings.LANGUAGE_CODE)

        backend = get_backend() 

        # This command is a NOOP if using the Mixpanel backend 
        if backend == 'app_metrics.backends.mixpanel': 
            print "Useless use of metrics_send_email when using Mixpanel backend."
            return 

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

        qs = MetricSet.objects.filter(Q(no_email=False), Q(send_daily=True) | Q(send_monthly=send_monthly) | Q(send_weekly=send_weekly))

        if "mailer" in settings.INSTALLED_APPS: 
            from mailer import send_html_mail 
            USE_MAILER = True 
        else: 
            from django.core.mail import EmailMultiAlternatives
            USE_MAILER = False 

        for s in qs: 
            subject = _("%s Report") % s.name 

            recipient_list = s.email_recipients.values_list('email', flat=True)
            
            (message, message_html) = generate_report(s, html=True)

            if message == None:
                continue

            if USE_MAILER: 
                send_html_mail(subject=subject, 
                               message=message, 
                               message_html=message_html, 
                               from_email=settings.DEFAULT_FROM_EMAIL, 
                               recipient_list=recipient_list)
            else: 
                msg = EmailMultiAlternatives(subject=subject,
                                             body=message,
                                             from_email=settings.DEFAULT_FROM_EMAIL,
                                             to=recipient_list)
                msg.attach_alternative(message_html, "text/html")
                msg.send()

        translation.deactivate()

