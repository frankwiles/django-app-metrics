========
Backends
========

.. attribute:: app_metrics.backends.db

    This backend stores all metrics and aggregations in your database. 
    
    .. admonition:: NOTE

        Every call to metric() generates a database write, which may 
        decrease your overall performance is you go nuts with them or have 
        a heavily traffic site.

.. _mixpanel_backend:

.. attribute:: app_metrics.backends.mixpanel

    This backend allows you to pipe all of your calls to metric() to Mixpanel.com 
    See http://mixpanel.com/api/docs/ for more information on their
