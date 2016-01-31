# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequestEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('method', models.CharField(max_length=6)),
                ('absolute_path', models.URLField()),
                ('is_ajax', models.BooleanField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
