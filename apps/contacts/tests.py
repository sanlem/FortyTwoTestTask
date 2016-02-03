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
                                           bio="bio\r\n!",
                                           other_contacts="bla\r\nbla")

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

        # check if we have br tag in conent
        self.assertIn("br", response.content)

        # ensure view had only returned Contacts
        self.assertTrue(isinstance(response.context['contacts'], Contacts))

        # if there are more than 1 contacts, should return the newest
        contacts = \
            Contacts(name="Myname",
                     lastname="Mylastname",
                     email="myemail",
                     date_of_birth=datetime.today(),
                     jabber_id="myjabber",
                     skype_login="myskype",
                     bio="bio!",
                     other_contacts="blabla")
        contacts.save()
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


class TestContactsEditView(TestCase):
    
    def setUp(self):
        # create contacts object
        self.contacts, created = \
            Contacts.objects.get_or_create(name="Myname",
                                           lastname="Mylastname",
                                           email="myemail",
                                           date_of_birth=datetime.today(),
                                           jabber_id="myjabber",
                                           skype_login="myskype",
                                           bio="bio\r\n!",
                                           other_contacts="bla\r\nbla")

        # remember client
        self.client = Client()

        # remember url
        self.url = reverse("contacts_edit")

    def test_contacts_edit_view(self):
        """ test contacts' edition """
        response = self.client.get(self.url)
        # ensure we have form on the page
        self.assertIn('<form', response.content)
        # ensure form has right method and url
        self.assertIn("action='" + reverse('contacts_edit') + "'", response.content)
        self.assertIn("method='POST'", response.content)
        # ensure there are control elements with Bootstrap classes
        self.assertIn('form-control', response.content)
        
        response = self.client.post(self.url, { name: 'Pavlo'})
        self.assertEqual(response.status_code, 200)
        # ensure the name is changed
        self.assertEqual(Contacts.objects.last().name, 'Pavlo')

        contacts = Contacts(name="Myname",
                            lastname="Mylastname",
                            email="myemail",
                            date_of_birth=datetime.today(),
                            jabber_id="myjabber",
                            skype_login="myskype",
                            bio="bio!",
                            other_contacts="blabla")

        # ensure view edits the newest object
        response = self.client.post(self.url, { name: 'Vitaliy'})
        self.assertEqual(Contacts.objects.get(2).name, 'Vitaliy')
        self.assertEqual(Contacts.objects.get(1).name, 'Pavlo')

        Contacts.objects.all().delete()
        # should render 'Can't edit. No contacts exist.'
        response = self.client.get(self.url)
        self.assertIn("Can't edit. No contacts exist.", response.content)
        # should return 400 status code
        response = self.client.post(self.url, { name: 'Vitaliy'})
        self.assertEqual(response.status_code, 400)
