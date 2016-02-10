# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RequestEntry.priority'
        db.add_column(u'requests_requestentry', 'priority',
                      self.gf('django.db.models.fields.IntegerField')(default=0, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RequestEntry.priority'
        db.delete_column(u'requests_requestentry', 'priority')


    models = {
        u'requests.requestentry': {
            'Meta': {'ordering': "['-priority', '-timestamp']", 'object_name': 'RequestEntry'},
            'absolute_path': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ajax': ('django.db.models.fields.BooleanField', [], {}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['requests']