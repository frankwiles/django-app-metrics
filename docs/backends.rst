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

    This backend allows you to pipe all of your calls to ``metric()`` to
    Mixpanel. See the `Mixpanel documentation`_ for more information on
    their API.

.. _`Mixpanel documentation`: http://mixpanel.com/docs/api-documentation

.. attribute:: app_metrics.backends.statsd

    This backend allows you to pipe all of your calls to ``metric()`` to a
    statsd server. See `statsd`_ for more information on their API.

.. _`statsd`: https://github.com/etsy/statsd

.. attribute:: app_metrics.backends.redis

    This backend allows you to use the metric() and gauge() aspects, but not
    timer aspects of app_metrics.

