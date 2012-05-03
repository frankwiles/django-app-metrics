import datetime

from django.db import models, IntegrityError
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Metric(models.Model):
    """ The type of metric we want to store """
    name    = models.CharField(max_length=50)
    slug    = models.SlugField(unique=True, max_length=60, db_index=True)

    class Meta:
        verbose_name = 'Metric'
        verbose_name_plural = 'Metrics'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slug = slugify(self.name)
            i = 0
            while True:
                try:
                    return super(Metric,self).save(*args, **kwargs)
                except IntegrityError:
                    i += 1
                    self.slug = "%s_%d" % (self, i)
        else:
            return super(Metric, self).save(*args, **kwargs)

class MetricSet(models.Model):
    """ A set of metrics that should be sent via email to certain users """
    name          = models.CharField(max_length=50)
    metrics       = models.ManyToManyField(Metric)
    email_recipients = models.ManyToManyField(User)
    no_email      = models.BooleanField(default=False)
    send_daily    = models.BooleanField(default=True)
    send_weekly   = models.BooleanField(default=False)
    send_monthly  = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Metric Set'
        verbose_name_plural = 'Metric Sets'

    def __unicode__(self):
        return self.name

class MetricItem(models.Model):
    """ Individual metric items """
    metric = models.ForeignKey(Metric)
    num  = models.IntegerField(default=1)
    created = models.DateField(default=datetime.datetime.now)

    class Meta:
        verbose_name = 'Metric Item'
        verbose_name_plural = 'Metric Items'

    def __unicode__(self):
        return "'%s' of %d on %s" % ( self.metric.name,
                                      self.num,
                                      self.created )

class MetricDay(models.Model):
    """ Aggregation of Metrics on a per day basis """
    metric  = models.ForeignKey(Metric)
    num   = models.BigIntegerField(default=0)
    created = models.DateField(default=datetime.date.today)

    class Meta:
        verbose_name = 'Day Metric'
        verbose_name_plural = 'By Day Metrics'

    def __unicode__(self):
        return "'%s' for '%s'" % (self.metric.name, self.created)

class MetricWeek(models.Model):
    """ Aggregation of Metrics on a weekly basis """
    metric  = models.ForeignKey(Metric)
    num   = models.BigIntegerField(default=0)
    created = models.DateField(default=datetime.date.today)

    class Meta:
        verbose_name = 'Week Metric'
        verbose_name_plural = 'By Week Metrics'

    def __unicode__(self):
        return "'%s' for week %s of %s" % (self.metric.name,
                                           self.created.strftime("%U"),
                                           self.created.strftime("%Y"))

class MetricMonth(models.Model):
    """ Aggregation of Metrics on monthly basis """
    metric  = models.ForeignKey(Metric)
    num   = models.BigIntegerField(default=0)
    created = models.DateField(default=datetime.date.today)

    class Meta:
        verbose_name = 'Month Metric'
        verbose_name_plural = 'By Month Metrics'

    def __unicode__(self):
        return "'%s' for %s %s" % (self.metric.name,
                                   self.created.strftime("%B"),
                                   self.created.strftime("%Y"))


class MetricYear(models.Model):
    """ Aggregation of Metrics on a yearly basis """
    metric  = models.ForeignKey(Metric)
    num   = models.BigIntegerField(default=0)
    created = models.DateField(default=datetime.date.today)

    class Meta:
        verbose_name = 'Year Metric'
        verbose_name_plural = 'By Year Metrics'

    def __unicode__(self):
        return "'%s' for month of '%s'" % (self.metric.name,
                                           self.created.strftime("%Y"))


