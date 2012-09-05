=====
Usage
=====

Example Code
============
The utility functions ``create_metric`` and ``metric`` are the main API hooks to app_metrics.

Example::

    from django.contrib.auth.models import User

    from app_metrics.utils import create_metric, metric

    user1 = User.objects.get(pk='bob')
    user2 = User.objects.get(pk='jane')

    # Create a new metric to track
    my_metric = create_metric(name='New User Metric', slug='new_user_signup')

    # Create a MetricSet which ties a metric to an email schedule and sets
    # who should receive it

    my_metric_set = create_metric_set(name='My Set',
                                    metrics=[my_metric],
                                    email_recipients=[user1, user2])

    # Increment the metric by one
    metric('new_user_signup')

    # Increment the metric by some other number
    metric('new_user_signup', 4)

    # Create a timer (only supported in statsd backend currently)
    with timing('mytimer'):
      for x in some_long_list:
         call_time_consuming_function(x)

    # Or if a context manager doesn't work for you you can use a Timer class
    t = Timer()
    t.start()
    something_that_takes_forever()
    t.stop()
    t.store('mytimer')

    # Gauges are current status type dials (think fuel gauge in a car)
    # These simply store and retrieve a value
    gauge('current_fuel', '30')
    guage('load_load', '3.14')

Management Commands
===================

metrics_aggregate
-----------------

Aggregate metric items into daily, weekly, monthly, and yearly totals
It's fairly smart about it, so you're safe to run this as often as you
like::

    manage.py metrics_aggregate

metrics_send_mail
-----------------

Send email reports to users. The email will be sent out using django_mailer_'s ``send_htmlmailer`` if it is installed, otherwise defaults to django.core.mail_. Can be called like::

    manage.py metrics_send_mail


.. _django_mailer: https://github.com/jtauber/django-mailer/
.. _django.core.mail: https://docs.djangoproject.com/en/dev/topics/email/
