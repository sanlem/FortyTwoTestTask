# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length='25')),
                ('lastname', models.CharField(max_length='25')),
                ('email', models.EmailField(max_length=254)),
                ('date_of_birth', models.DateField()),
                ('jabber_id', models.CharField(blank=True, max_length=25, null=True)),
                ('skype_login', models.CharField(blank=True, max_length=25, null=True)),
                ('bio', models.TextField(blank=True, max_length=300, null=True)),
                ('other_contacts', models.TextField(blank=True, max_length=300, null=True)),
            ],
        ),
    ]
