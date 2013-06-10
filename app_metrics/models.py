import datetime
import logging

from django.conf import settings
from django import forms
from django.db import models, IntegrityError
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

import bitfield


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


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
    email_recipients = models.ManyToManyField(USER_MODEL, verbose_name=_('email recipients'))
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


class MyBitFormField(forms.IntegerField):
    """
    Once issue 28 is fixed upstream, this override isn't needed
    https://github.com/disqus/django-bitfield/issues/28
    """
    def __init__(self, choices=(), widget=bitfield.forms.BitFieldCheckboxSelectMultiple, *args, **kwargs):
        if isinstance(kwargs['initial'],int):
            iv = kwargs['initial']
            l = []
            for i in range(0, 63):
               if (1<<i) & iv > 0:
                       l += [choices[i][0]]
            kwargs['initial'] = l
        self.widget = widget
        super(MyBitFormField, self).__init__(widget=widget, *args, **kwargs)
        self.choices = self.widget.choices = choices

    def clean(self, value):
        if not value:
            return 0

        # Assume an iterable which contains an item per flag that's enabled
        result = bitfield.BitHandler(0, [k for k, v in self.choices])
        for k in value:
            try:
                setattr(result, str(k), True)
            except AttributeError:
                raise forms.ValidationError('Unknown choice: %r' % (k,))
        return int(result)


class ThresholdActiveManager(models.Manager):

    def get_query_set(self):
        return super(ThresholdActiveManager, self).get_query_set().filter(is_active=True)
 

class DayChoiceField(bitfield.BitField):
    """
    Custom field to store days of the week
    """
    MONDAY = 'monday'
    TUESDAY = 'tuesday'
    WEDNESDAY = 'wednesday'
    THURSDAY = 'thursday'
    FRIDAY = 'friday'
    SATURDAY = 'saturday'
    SUNDAY = 'sunday'
    flags = (MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY)
    default = (MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY)

    def __init__(self, *args, **kwargs):
        super(DayChoiceField, self).__init__(flags=DayChoiceField.flags, default=DayChoiceField.default, *args, **kwargs)

    def formfield(self, form_class=MyBitFormField, **kwargs):
        return super(DayChoiceField, self).formfield(form_class=form_class, **kwargs)

    @staticmethod
    def flags_as_weekdays(field):
        """
        Helper function for DayChoiceField
        Due to the construction on that field I cannot use it on an instance
        """
        days = []
        mapping = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3,
                'friday': 4, 'saturday': 5, 'sunday': 6}
        for f in field:
            if f[1]:
                days.append(mapping.get(f[0]))
        return days


class Threshold(models.Model):
    """
    Will throw a logging error if threshold is broken
    """
    TIME_MINS = 1
    TIME_HOURS = 2
    TIME_DAYS = 3
    TIME_CHOICES = (
        (TIME_MINS, 'Minutes'),
        (TIME_HOURS, 'Hours'),
        (TIME_DAYS, 'Days'),
    )
    THRESHOLD_BELOW = 1
    THRESHOLD_ABOVE = 2
    THRESHOLD_CHOICES = (
        (THRESHOLD_BELOW, 'Below'),
        (THRESHOLD_ABOVE, 'Above'),
    )
    name = models.CharField(_('name'), max_length=50)
    metric = models.ForeignKey('Metric')
    is_active = models.BooleanField(default=True)
    time_measurement = models.IntegerField(choices=TIME_CHOICES)
    time_amount = models.IntegerField()
    threshold_amount = models.IntegerField()
    threshold_direction = models.IntegerField(choices=THRESHOLD_CHOICES)
    applies_for_days = DayChoiceField()
    exclude_hour_start = models.IntegerField(help_text=_('0-24, Hour of the Day'), null=True, blank=True)
    exclude_hour_end = models.IntegerField(help_text=_('0-24, Hour of the Day'), null=True, blank=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    objects = models.Manager()
    active = ThresholdActiveManager()

    class Meta:
        verbose_name = _('threshold')
        verbose_name_plural = _('threshold')

    def __init__(self, logger=None, *args, **kwargs):
        super(Threshold, self).__init__(*args, **kwargs)
        if logger is None:
            logger = logging.getLogger('app_metrics')
        self.set_logger(logger)

    def set_logger(self, logger):
        if isinstance(logger, logging.Logger):
            self._logger = logger
        else:
            raise Exception('%s is not a Logger' % logger)

    def __unicode__(self):
        return self.name

    @property
    def describe(self):
        """
        Formatted description of the threshold, used for logging in case of a failure
        """
        d = {'name': self.name, 'metric': self.metric, 'direction': self.get_threshold_direction_display(), 'amount': self.threshold_amount, 'time': self.time_amount, 'measurement': self.time_measurement }
        return "%(name)s (%(metric)s) - %(direction)s %(amount)d for %(time)d %(measurement)s" % d

    def _get_time_lower_bound(self, now):
        kwargs = {}
        if self.time_measurement == self.TIME_MINS:
            kwargs['minutes'] = self.time_amount
        if self.time_measurement == self.TIME_HOURS:
            kwargs['hours'] = self.time_amount
        if self.time_measurement == self.TIME_DAYS:
            kwargs['days'] = self.time_amount
        diff = datetime.timedelta(**kwargs)
        return now - diff

    def _is_excluded(self, now):
        # test for which days apply
        if self.applies_for_days:
            if now.weekday() not in DayChoiceField.flags_as_weekdays(self.applies_for_days):
                return True
        # test for exclusionary time
        if self.exclude_hour_start and self.exclude_hour_end:
            exclude_start = datetime.datetime(now.year, now.month, now.day, self.exclude_hour_start, 0)
            exclude_end = datetime.datetime(now.year, now.month, now.day, self.exclude_hour_end, 0)
            if exclude_start < now and exclude_end > now:
                return True
            # test for if looking back will fall into exclusionary time
            if self.time_measurement == self.TIME_DAYS:
                return False  # ignoring this test, as exclusions are in hours, it will always pass
            history_lookup_start = self._get_time_lower_bound(now)
            if exclude_start < history_lookup_start and exclude_end > history_lookup_start:
                return True
        return False

    def get_metric_total_in_period(self, now=None):
        if now is None:
            now = datetime.datetime.now()
        exclude_start = self._get_time_lower_bound(now)
        exclude_end = now
        total = 0
        # need to check both individual metrics that have not been aggregated, and those that have been
        clean = lambda x: int(x or 0)
        total += clean(MetricItem.objects.filter(metric=self.metric, created__range=(exclude_start, exclude_end)).aggregate(models.Sum('num')).get('num__sum', 0))
        total += clean(MetricDay.objects.filter(metric=self.metric, created__range=(exclude_start, exclude_end)).aggregate(models.Sum('num')).get('num__sum', 0))
        return total

    def reached(self, now=None):
        if now is None:
            now = datetime.datetime.now()
        if self._is_excluded(now):
            return None
        total = self.get_metric_total_in_period(now)
        if self.threshold_direction == self.THRESHOLD_BELOW:
            if total < self.threshold_amount:
                self._logger.error(self.describe)
                return False
        elif self.threshold_direction == self.THRESHOLD_ABOVE:
            if total > self.threshold_amount:
                self._logger.error(self.describe)
                return False
        return True 
