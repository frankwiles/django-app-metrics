import datetime

from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _


class Metric(models.Model):
    """ The type of metric we want to store """
    name = models.CharField(_('name'), max_length=50)
    slug = models.SlugField(_('slug'), unique=True, max_length=60, db_index=True)

    class Meta:
        verbose_name = _('metric')
        verbose_name_plural = _('metrics')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
            i = 0
            while True:
                try:
                    return super(Metric, self).save(*args, **kwargs)
                except IntegrityError:
                    i += 1
                    self.slug = "%s_%d" % (self.slug, i)
        else:
            return super(Metric, self).save(*args, **kwargs)

class MetricSet(models.Model):
    """ A set of metrics that should be sent via email to certain users """
    name = models.CharField(_('name'), max_length=50)
    metrics = models.ManyToManyField(Metric, verbose_name=_('metrics'))
    email_recipients = models.ManyToManyField(User, verbose_name=_('email recipients'))
    no_email = models.BooleanField(_('no e-mail'), default=False)
    send_daily = models.BooleanField(_('send daily'), default=True)
    send_weekly = models.BooleanField(_('send weekly'), default=False)
    send_monthly = models.BooleanField(_('send monthly'), default=False)

    class Meta:
        verbose_name = _('metric set')
        verbose_name_plural = _('metric sets')

    def __unicode__(self):
        return self.name

class MetricItem(models.Model):
    """ Individual metric items """
    metric = models.ForeignKey(Metric, verbose_name=_('metric'))
    num = models.IntegerField(_('number'), default=1)
    created = models.DateTimeField(_('created'), default=datetime.datetime.now)

    class Meta:
        verbose_name = _('metric item')
        verbose_name_plural = _('metric items')

    def __unicode__(self):
        return _("'%(name)s' of %(num)d on %(created)s") % {
            'name': self.metric.name,
            'num': self.num,
            'created': self.created
        }

class MetricDay(models.Model):
    """ Aggregation of Metrics on a per day basis """
    metric = models.ForeignKey(Metric, verbose_name=_('metric'))
    num = models.BigIntegerField(_('number'), default=0)
    created = models.DateField(_('created'), default=datetime.date.today)

    class Meta:
        verbose_name = _('day metric')
        verbose_name_plural = _('day metrics')

    def __unicode__(self):
        return _("'%(name)s' for '%(created)s'") % {
            'name': self.metric.name,
            'created': self.created
        }

class MetricWeek(models.Model):
    """ Aggregation of Metrics on a weekly basis """
    metric = models.ForeignKey(Metric, verbose_name=_('metric'))
    num = models.BigIntegerField(_('number'), default=0)
    created = models.DateField(_('created'), default=datetime.date.today)

    class Meta:
        verbose_name = _('week metric')
        verbose_name_plural = _('week metrics')

    def __unicode__(self):
        return _("'%(name)s' for week %(week)s of %(year)s") % {
            'name': self.metric.name,
            'week': self.created.strftime("%U"),
            'year': self.created.strftime("%Y")
        }

class MetricMonth(models.Model):
    """ Aggregation of Metrics on monthly basis """
    metric = models.ForeignKey(Metric, verbose_name=('metric'))
    num = models.BigIntegerField(_('number'), default=0)
    created = models.DateField(_('created'), default=datetime.date.today)

    class Meta:
        verbose_name = _('month metric')
        verbose_name_plural = _('month metrics')

    def __unicode__(self):
        return _("'%(name)s' for %(month)s %(year)s") % {
            'name': self.metric.name,
            'month': self.created.strftime("%B"),
            'year': self.created.strftime("%Y")
        }


class MetricYear(models.Model):
    """ Aggregation of Metrics on a yearly basis """
    metric = models.ForeignKey(Metric, verbose_name=_('metric'))
    num = models.BigIntegerField(_('number'), default=0)
    created = models.DateField(_('created'), default=datetime.date.today)

    class Meta:
        verbose_name = _('year metric')
        verbose_name_plural = _('year metrics')

    def __unicode__(self):
        return _("'%(name)s' for %(year)s") % {
            'name': self.metric.name,
            'year': self.created.strftime("%Y")
        }


class Gauge(models.Model):
    """
    A representation of the current state of some data.
    """
    name = models.CharField(_('name'), max_length=50)
    slug = models.SlugField(_('slug'), unique=True, max_length=60)
    current_value = models.DecimalField(_('current value'), max_digits=15, decimal_places=6, default='0.00')
    created = models.DateTimeField(_('created'), default=datetime.datetime.now)
    updated = models.DateTimeField(_('updated'), default=datetime.datetime.now)

    class Meta:
        verbose_name = _('gauge')
        verbose_name_plural = _('gauges')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)

        self.updated = datetime.datetime.now()
        return super(Gauge, self).save(*args, **kwargs)
