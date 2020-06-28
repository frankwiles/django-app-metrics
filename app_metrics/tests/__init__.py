from celery import current_app


current_app.conf.CELERY_ALWAYS_EAGER = True
current_app.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
