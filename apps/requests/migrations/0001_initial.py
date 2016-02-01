# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RequestEntry'
        db.create_table(u'requests_requestentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('absolute_path', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('is_ajax', self.gf('django.db.models.fields.BooleanField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'requests', ['RequestEntry'])


    def backwards(self, orm):
        # Deleting model 'RequestEntry'
        db.delete_table(u'requests_requestentry')


    models = {
        u'requests.requestentry': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'RequestEntry'},
            'absolute_path': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ajax': ('django.db.models.fields.BooleanField', [], {}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['requests']