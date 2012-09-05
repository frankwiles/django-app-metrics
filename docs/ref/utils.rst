=================
Utility Functions
=================

``create_metric``
=================

.. function:: create_metric(name, slug)
    
    Creates a new type of metric track

Arguments
---------

``name``
    The verbose name of the metric to track

``slug``
    The identifying slug used for the metric. This is what is passed into :func:`metric` to increment the metric


``metric``
==========
.. function::  metric(slug, num=1, \*\*kwargs)

    Increment a metric by ``num``

    Shortcut to the current backend (as set by :attr:`APP_METRICS_BACKEND` metric method.)  
    
.. admonition:: Note

    If there is no metric mapped to ``slug``, a metric named ``Autocreated Metric`` with the passed in``slug`` will be auto-generated.

Arguments
---------

``slug`` `(required)`
    Name of the metric to increment.

``num``
    Number to increment the metric by. Defaults to 1.

``create_metric_set``
=====================

.. function:: create_metric_set(create_metric_set(name=None, metrics=None, email_recipients=None, no_email=False, send_daily=True, send_weekly=False, send_monthly=False)

   Creates a new metric set 

Arguments
---------

``name``
    Verbose name given to the new metric_set

``metrics``
    Iterable of slugs that the metric set should collect
    
``email_recipients``
    Iterable of Users_ who should be emailed with updates on the metric set 

.. _Users: https://docs.djangoproject.com/en/1.3/topics/auth/#django.contrib.auth.models.User
    
