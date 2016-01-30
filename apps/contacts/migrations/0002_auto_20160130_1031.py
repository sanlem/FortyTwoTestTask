# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import migrations, models
from datetime import datetime


def create_superuser(apps, schema_editor):
    # data migration which creates initial superuser
    # User = apps.get_model("auth", "User")
    superuser, created = User.objects.get_or_create(username="admin")
    if created:
        superuser.email = "admin@42cc.com"
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.set_password("admin")
        superuser.save()

def create_initial_contacts(apps, schema_editor):
    Contacts = apps.get_model("contacts", "Contacts")
    contacts = Contacts(name="Myname",
                        lastname="Mylastname",
                        email="myemail",
                        date_of_birth=datetime.today(),
                        jabber_id="myjabber",
                        skype_login="myskype",
                        bio="bio!",
                        other_contacts="blabla")
    contacts.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
        migrations.RunPython(create_initial_contacts),
    ]
