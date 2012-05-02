from app_metrics.tests.base_tests import *
from app_metrics.tests.mixpanel_tests import *

try:
    import statsd
except ImportError:
    print "Skipping the statsd tests."
    statsd = None

if statsd is not None:
    from app_metrics.tests.statsd_tests import *
