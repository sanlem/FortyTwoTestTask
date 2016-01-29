from django.db import models


class Contacts(models.Model):
    name = models.CharField(max_length="25")
    lastname = models.CharField(max_length="25")
    email = models.EmailField()
    date_of_birth = models.DateField()
    jabber_id = models.CharField(max_length=25, null=True, blank=True)
    skype_login = models.CharField(max_length=25, null=True, blank=True)
    bio = models.TextField(max_length=300, null=True, blank=True)
    other_contacts = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return "%s %s's contacts" % (self.name, self.lastname)
