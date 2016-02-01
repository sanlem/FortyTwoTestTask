# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        from django.core.management import call_command
        call_command("loaddata", "data.json")

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'contacts.contacts': {
            'Meta': {'object_name': 'Contacts'},
            'bio': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'other_contacts': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'skype_login': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['contacts']
    symmetrical = True
