
Settings: 
APP_METRIC_BACKEND='app-metrics.backends.db'

Usage: 

  from app_metrics.utils import create_metric, metric

  # Create a new metric to track 
  create_metric(
       name='New User Metric',
       slug='new_user_signup', 
       email_recipients = [user1, user2],
       no_email=True) 

  # Increment the metric by one 
  metric('new_user_signup') 

  # Increment the metric by some other number 
  metric('new_user_signup', 4) 

  manage.py metrics_aggregate 
  manage.py metrics_send_mail 

