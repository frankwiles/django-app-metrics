from django.conf.urls import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
        (r'^admin/', include(admin.site.urls)),
        (r'^admin/metrics/', include('app_metrics.urls')),
)
