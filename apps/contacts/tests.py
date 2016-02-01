from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from apps.contacts.models import Contacts
from datetime import datetime


class TestContactsView(TestCase):

    def setUp(self):
        # create contacts object
        self.contacts, created = \
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

        # check if we have correct name in content
        self.assertIn(self.contacts.name, response.content)

        # check if we have "Bio:" label in content
        self.assertIn("Bio:", response.content)

        # ensure view had only returned Contacts
        self.assertTrue(isinstance(response.context['contacts'], Contacts))

        # if there are more than 1 contacts, should return the newest
        contacts, created = \
            Contacts.objects.get_or_create(name="Myname",
                                           lastname="Mylastname",
                                           email="myemail",
                                           date_of_birth=datetime.today(),
                                           jabber_id="myjabber",
                                           skype_login="myskype",
                                           bio="bio!",
                                           other_contacts="blabla")
        response = self.client.get(self.url)
        self.assertEqual(response.context['contacts'].id, 2)

        # should render 'No contacts.' if aren't any
        Contacts.objects.all().delete()
        response = self.client.get(self.url)
        self.assertIn('No contacts.', response.content)


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
