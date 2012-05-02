import sys
from django.core.management.base import NoArgsCommand
from app_metrics.models import MetricItem
from app_metrics.backends.statsd_backend import metric


class Command(NoArgsCommand):
    help = "Move MetricItems from the db backend to statsd"
    requires_model_validation = True

    def handle_noargs(self, **options):
        """Move MetricItems from the db backend to statsd"""
        backend = get_backend()

        # If not using statsd, this command is a NOOP.
        if backend != 'app_metrics.backends.statsd_backend':
            sys.exit(1, "You need to set the backend to 'statsd_backend'")

        items = MetricItem.objects.all()

        for i in items:
            metric(i.metric.slug, num=i.num)

        # Kill off our items
        items.delete()
