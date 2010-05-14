
Overview
========

django-app-metrics is a in-development project to capture and report on various
possible events in your application.  You simply define various named metrics
and record when they happen.  These might be certain events that may be
immediatey useful, for example 'New User Signups', 'Downloads', etc. 

Or they might not prove useful until some point in the future.  But if you 
begin recording them now you'll have great data later on when you do need it. 
For example 'Total Items Sold' isn't an exciting number when you're just
launching when you only care about revenue, but being able to do a contest 
for the 1 millionth sold item in the future you'll be glad you were tracking 
it. 

You then group these individual metrics into a MetricSet, where you define
how often you want an email report being sent, and to which User(s) it should 
be sent. 

Settings 
========

APP_METRIC_BACKEND='app-metrics.backends.db' currently our only backend.
The plan is to add in redis and celery capture and aggregation as well in the
future. NOTE: Every call to metric() generates a data write, which may decrease
your overall performance is you go nuts with them or have a large site. 

Usage 
=====

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

TODO
====

    - Improve text and HTML templates to display trending data well 
    - Create redis backend for collection and aggregation 
    - Create celery backend for collection and aggregation 


