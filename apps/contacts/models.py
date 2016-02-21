from django.db import models
from PIL import Image
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class Contacts(models.Model):
    name = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    email = models.EmailField()
    date_of_birth = models.DateField()
    jabber_id = models.CharField(max_length=25, null=True, blank=True)
    skype_login = models.CharField(max_length=25, null=True, blank=True)
    bio = models.TextField(max_length=300, null=True, blank=True)
    other_contacts = models.TextField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)

    def __unicode__(self):
        return "%s %s's contacts" % (self.name, self.lastname)

    def save(self, *args, **kwargs):
        if self.image:
            image = Image.open(StringIO.StringIO(self.image.read()))
            image.thumbnail((200, 200), Image.ANTIALIAS)
            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)

            name = self.image.name
            if 'jpeg' not in name:
                name = name[:name.rindex('.') + 1] + 'jpeg'
            self.image = InMemoryUploadedFile(output, 'ImageField',
                                              name, 'image/jpeg',
                                              output.len, None)

            # delete old image
            try:
                # we need to refresh object
                this = Contacts.objects.get(id=self.id)
                if this.image != self.image:
                    this.image.delete(False)
            except:
                pass

        super(Contacts, self).save(*args, **kwargs)


class ChangeEntry(models.Model):
    model_name = models.CharField(max_length=25)
    action = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    instance_id = models.IntegerField()
