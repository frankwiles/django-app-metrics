# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Metric'
        db.create_table('app_metrics_metric', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=60)),
        ))
        db.send_create_signal('app_metrics', ['Metric'])

        # Adding model 'MetricSet'
        db.create_table('app_metrics_metricset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('no_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('send_daily', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('send_weekly', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('send_monthly', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('app_metrics', ['MetricSet'])

        # Adding M2M table for field metrics on 'MetricSet'
        db.create_table('app_metrics_metricset_metrics', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('metricset', models.ForeignKey(orm['app_metrics.metricset'], null=False)),
            ('metric', models.ForeignKey(orm['app_metrics.metric'], null=False))
        ))
        db.create_unique('app_metrics_metricset_metrics', ['metricset_id', 'metric_id'])

        # Adding M2M table for field email_recipients on 'MetricSet'
        db.create_table('app_metrics_metricset_email_recipients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('metricset', models.ForeignKey(orm['app_metrics.metricset'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('app_metrics_metricset_email_recipients', ['metricset_id', 'user_id'])

        # Adding model 'MetricItem'
        db.create_table('app_metrics_metricitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_metrics.Metric'])),
            ('num', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('app_metrics', ['MetricItem'])

        # Adding model 'MetricDay'
        db.create_table('app_metrics_metricday', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_metrics.Metric'])),
            ('num', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal('app_metrics', ['MetricDay'])

        # Adding model 'MetricWeek'
        db.create_table('app_metrics_metricweek', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_metrics.Metric'])),
            ('num', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal('app_metrics', ['MetricWeek'])

        # Adding model 'MetricMonth'
        db.create_table('app_metrics_metricmonth', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_metrics.Metric'])),
            ('num', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal('app_metrics', ['MetricMonth'])

        # Adding model 'MetricYear'
        db.create_table('app_metrics_metricyear', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_metrics.Metric'])),
            ('num', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal('app_metrics', ['MetricYear'])

    def backwards(self, orm):
        # Deleting model 'Metric'
        db.delete_table('app_metrics_metric')

        # Deleting model 'MetricSet'
        db.delete_table('app_metrics_metricset')

        # Removing M2M table for field metrics on 'MetricSet'
        db.delete_table('app_metrics_metricset_metrics')

        # Removing M2M table for field email_recipients on 'MetricSet'
        db.delete_table('app_metrics_metricset_email_recipients')

        # Deleting model 'MetricItem'
        db.delete_table('app_metrics_metricitem')

        # Deleting model 'MetricDay'
        db.delete_table('app_metrics_metricday')

        # Deleting model 'MetricWeek'
        db.delete_table('app_metrics_metricweek')

        # Deleting model 'MetricMonth'
        db.delete_table('app_metrics_metricmonth')

        # Deleting model 'MetricYear'
        db.delete_table('app_metrics_metricyear')

    models = {
        'app_metrics.metric': {
            'Meta': {'object_name': 'Metric'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '60'})
        },
        'app_metrics.metricday': {
            'Meta': {'object_name': 'MetricDay'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_metrics.Metric']"}),
            'num': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'app_metrics.metricitem': {
            'Meta': {'object_name': 'MetricItem'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_metrics.Metric']"}),
            'num': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'app_metrics.metricmonth': {
            'Meta': {'object_name': 'MetricMonth'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_metrics.Metric']"}),
            'num': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'app_metrics.metricset': {
            'Meta': {'object_name': 'MetricSet'},
            'email_recipients': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metrics': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app_metrics.Metric']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'no_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'send_daily': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_monthly': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'send_weekly': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'app_metrics.metricweek': {
            'Meta': {'object_name': 'MetricWeek'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_metrics.Metric']"}),
            'num': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'app_metrics.metricyear': {
            'Meta': {'object_name': 'MetricYear'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_metrics.Metric']"}),
            'num': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app_metrics']