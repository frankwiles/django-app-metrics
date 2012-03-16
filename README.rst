Overview
========

django-app-metrics allows you to capture and report on various events in your
applications.  You simply define various named metrics and record when they
happen.  These might be certain events that may be immediatey useful, for
example 'New User Signups', 'Downloads', etc.

Or they might not prove useful until some point in the future.  But if you
begin recording them now you'll have great data later on if you do need it.

For example 'Total Items Sold' isn't an exciting number when you're just
launching when you only care about revenue, but being able to do a contest
for the 1 millionth sold item in the future you'll be glad you were tracking
it.

You then group these individual metrics into a MetricSet, where you define
how often you want an email report being sent, and to which User(s) it should
be sent.

Requirements
============

Celery_ and `django-celery`_ must be installed, however if you do not wish to
actually use Celery you can simply set ``CELERY_ALWAYS_EAGER = True`` in your
settings and it will behave as if Celery was not configured.

.. _Celery: http://celeryproject.org/
.. _`django-celery`: http://ask.github.com/django-celery/

Usage
=====

::

  from app_metrics.utils import create_metric, metric

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

  # Aggregate metric items into daily, weekly, monthly, and yearly totals
  # It's fairly smart about it, so you're safe to run this as often as you
  # like
  manage.py metrics_aggregate

  # Send email reports to users
  manage.py metrics_send_mail

Backends
========

``app_metrics.backends.db`` (Default) - This backend stores all metrics and
aggregations in your database. NOTE: Every call to ``metric()`` generates a
database write, which may decrease your overall performance is you go nuts
with them or have a heavily traffic site.

``app_metrics.backends.mixpanel`` - This backend allows you to pipe all of
your calls to ``metric()`` to Mixpanel. See the `Mixpanel documentation`_
for more information on their API.

.. _`Mixpanel documentation`: http://mixpanel.com/docs/api-documentation

Settings
========

``APP_METRICS_BACKEND`` - Defaults to 'app_metrics.backends.db' if not defined.

``APP_METRICS_MIXPANEL_TOKEN`` - Your Mixpanel.com API token

``APP_METRICS_MIXPANEL_URL`` - Allow overriding of the API URL end point

``APP_METRICS_SEND_ZERO_ACTIVITY`` - Prevent e-mails being sent when there's been 
no activity today (i.e. during testing). Defaults to `True`.

TODO
====

- Improve text and HTML templates to display trending data well
- Create redis backend for collection and aggregation

