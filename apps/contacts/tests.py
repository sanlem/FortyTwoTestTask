from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from apps.contacts.models import Contacts
from datetime import datetime

class TestContactsView(TestCase):
    
    def setUp(self):
        # create contacts object
        contacts, created = Contacts.get_or_create(name="Myname", lastname="Mylastname", email="myemail", \
            date_of_birth=datetime.datetime.now().date(), jabber_id="myjabber", skype_login="myskype", bio="bio!", other_contacts="blabla")

        # remember client
        self.client = Client()

        # remember url
        self.url = reverse("home")

    def test_contacts_list(self):
        response = self.client.get(self.url)

        # checking response's status code
        self.assertEqual(response.status_code, 200)

        # check if we have 'Myname' in content
        self.assertIn("Myname", response.content)

        # check if we have "Bio:" label in content
        self.assertIn("Bio:", response.content)

        # ensure we have only one contacts object this time
        self.assertEqual(len(response.context['contacts']), 1)