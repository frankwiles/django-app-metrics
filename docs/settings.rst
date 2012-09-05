.. _settings:

========
Settings
========


Base Settings
=============
.. attribute:: APP_METRICS_BACKEND

    Defaults to :attr:`app_metrics.backends.db` if not defined.

Mixpanel Backend Settings
=========================
These settings are only necessary if you're using the :ref:`Mixpanel backend<mixpanel_backend>`

.. attribute:: APP_METRICS_MIXPANEL_TOKEN

    Your Mixpanel.com API token

.. attribute:: APP_METERICS_MIXPANEL_URL

    Allow overriding of the API URL end point

Statsd Settings
===============

.. attribute:: APP_METRICS_STATSD_HOST

    Hostname of statsd server, defaults to 'localhost'

.. attribute:: APP_METRICS_STATSD_PORT

    statsd port, defaults to '8125'

.. attribute:: APP_METRICS_STATSD_SAMPLE_RATE

    statsd sample rate, defaults to 1

Redis Settings
==============

.. attribute:: APP_METRICS_REDIS_HOST

    Hostname of redis server, defaults to 'localhost'

.. attribute:: APP_METRICS_REDIS_PORT

    redis port, defaults to '6379'

.. attribute:: APP_METRICS_REDIS_DB

    redis database number to use, defaults to 0
