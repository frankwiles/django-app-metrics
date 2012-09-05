============
Installation
============

Installing
==========

* Install with pip::

    pip install git+https://github.com/frankwiles/django-app-metrics.git

* Add ``app_metrics`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS =
        # ...
        'app_metrics',
    )

* Edit :ref:`settings` in your project's settings module to your liking

Requirements
============
celery and django-celery must be installed, however if you do not wish to
actually use celery you can simply set CELERY_ALWAYS_EAGER = True in your
settings and it will behave as if celery was not configured.

