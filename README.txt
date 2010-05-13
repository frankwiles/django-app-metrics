
Settings: 
APP_METRIC_BACKEND='app-metrics.backends.db'

Usage: 

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

  # Send email reports to users (TODO)
  manage.py metrics_send_mail 

