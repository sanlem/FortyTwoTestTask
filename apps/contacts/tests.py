from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from apps.contacts.models import Contacts
from datetime import datetime


class TestContactsView(TestCase):

    def setUp(self):
        # create contacts object
        contacts, created = \
            Contacts.objects.get_or_create(name="Myname",
                                           lastname="Mylastname",
                                           email="myemail",
                                           date_of_birth=datetime.today(),
                                           jabber_id="myjabber",
                                           skype_login="myskype",
                                           bio="bio!",
                                           other_contacts="blabla")

        # remember client
        self.client = Client()

        # remember url
        self.url = reverse("contacts_list")

    def test_contacts_list(self):
        """ testing contacts list view """
        response = self.client.get(self.url)

        # checking response's status code
        self.assertEqual(response.status_code, 200)

        # check if we have 'Myname' in content
        # self.assertIn(bytes("Myname", 'utf-8'), response.content)
        self.assertIn("Myname", response.content)

        # check if we have "Bio:" label in content
        # self.assertIn(bytes("Bio:", 'utf-8'), response.content)
        self.assertIn("Bio:", 'utf-8'), response.content)

        # ensure we have only one contacts object this time
        self.assertEqual(len(response.context['contacts']), 1)


class TestContactsModel(TestCase):

    def test_str(self):
        """ only custom methods need to be tested """
        contacts = Contacts(name="Myname",
                            lastname="Mylastname",
                            email="myemail",
                            date_of_birth=datetime.today(),
                            jabber_id="myjabber",
                            skype_login="myskype",
                            bio="bio!",
                            other_contacts="blabla")

        self.assertEqual(str(contacts), "Myname Mylastname's contacts")
