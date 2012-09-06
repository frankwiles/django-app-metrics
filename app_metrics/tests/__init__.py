from app_metrics.tests.base_tests import *
from app_metrics.tests.mixpanel_tests import *

try:
    import statsd
except ImportError:
    print "Skipping the statsd tests."
    statsd = None

if statsd is not None:
    from app_metrics.tests.statsd_tests import *

try:
    import redis
except ImportError:
    print "Skipping redis tests."
    redis = None

if redis is not None:
    from app_metrics.tests.redis_tests import *

#try:
#    import librato
#except ImportError:
#    print "Skipping librato tests..."
#    librato = None
#
#if librato is not None:
#    from app_metrics.tests.librato_tests import *
