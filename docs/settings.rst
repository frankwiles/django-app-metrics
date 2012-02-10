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

