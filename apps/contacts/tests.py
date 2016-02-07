from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from apps.contacts.models import Contacts
from datetime import datetime, date
from apps.contacts.forms import ContactsEditForm
from django.contrib.auth.models import User


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

update_dict = {
    'name': 'Pavlo',
    'lastname': 'Samboruk',
    'email': 'asd@ex.com',
    'date_of_birth': date.today()
}


class TestContactsEditView(TestCase):

    def setUp(self):
        # create contacts object
        self.contacts, created = \
            Contacts.objects.get_or_create(name="Myname",
                                           lastname="Mylastname",
                                           email="myemail@email.com",
                                           date_of_birth=datetime.today(),
                                           jabber_id="myjabber",
                                           skype_login="myskype",
                                           bio="bio\r\n!",
                                           other_contacts="bla\r\nbla")
        # creating user to log it in
        u = User(username='admin')
        u.set_password('admin')
        u.save()

        # remember client
        self.client = Client()

        # remember url
        self.url = reverse("contacts_edit")

        # remember image
        self.image = open('./assets/test_image.png')

    def test_contacts_edit_view(self):
        """ test contacts' edition """
        response = self.client.get(self.url)
        # not authenticated
        url = reverse('login') + '?next=/edit/'
        self.assertRedirects(response, url, status_code=302)
        self.client.login(username='admin', password='admin')
        # authenticated now
        response = self.client.get(self.url)
        # ensure we have form on the page
        self.assertIn('<form', response.content)
        # ensure the form's media is loaded
        self.assertIn(str(ContactsEditForm().media), response.content)
        # ensure form has right method and url
        self.assertIn("action='" + reverse('contacts_edit') + "'",
                      response.content)
        self.assertIn("method='POST'", response.content)
        # ensure there are control elements with Bootstrap classes
        self.assertIn('form-control', response.content)
        # ensure enctype is correct
        self.assertIn('enctype="multipart/form-data"', response.content)
        # ensure our contacts are loaded
        self.assertEqual(response.context['object'], self.contacts)
        # end fields are filled with proper data
        self.assertIn('Myname', response.content)
        self.assertIn('Mylastname', response.content)

        response = self.client.post(self.url, update_dict)
        self.assertEqual(response.status_code, 302)
        # ensure the name is changed
        self.assertEqual(Contacts.objects.get(pk=1).name, 'Pavlo')

        contacts = Contacts(name="Myname",
                            lastname="Mylastname",
                            email="myemail",
                            date_of_birth=datetime.today(),
                            jabber_id="myjabber",
                            skype_login="myskype",
                            bio="bio!",
                            other_contacts="blabla")
        contacts.save()

        params = update_dict.copy()
        params['name'] = 'Vitaliy'
        params['lastname'] = 'Franchook'
        # ensure view edits the newest object
        response = self.client.post(self.url, params)
        self.assertEqual(Contacts.objects.get(pk=2).name, 'Vitaliy')
        self.assertEqual(Contacts.objects.get(pk=1).name, 'Pavlo')

        Contacts.objects.all().delete()
        # should render 'Can't edit. No contacts exist.'
        response = self.client.get(self.url)
        self.assertIn("Can't edit. No contacts exist.", response.content)
        # should return 400 status code for post requests if no objects
        response = self.client.post(self.url, {'name': 'Vitaliy'})
        self.assertEqual(response.status_code, 400)

    def test_image_upload(self):
        """ some tests for image uploading """
        self.client.login(username='admin', password='admin')
        params = update_dict.copy()
        params.update({'image': self.image})
        response = self.client.post(reverse('contacts_edit'), params)
        # redirect if success
        contacts = Contacts.objects.last()
        self.assertEqual(response.status_code, 302)
        # check if image was scaled
        self.assertTrue(contacts.image.width <= 200)
        self.assertTrue(contacts.image.height <= 200)
        # check if it is jpeg now
        self.assertIn('jpeg', contacts.image.name)


class TestAuth(TestCase):

    def setUp(self):
        # remember User
        self.user = User(username='sanlem')
        self.password = '11111'
        self.user.set_password(self.password)
        self.user.save()

        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

        self.client = Client()

    def test_login_and_logout(self):
        """ test auth """
        response = self.client.post(self.login_url,
                                    {'username': self.user.username,
                                     'password': 'wrong_password'})
        # credentials are wrong
        self.assertTrue(response.context['user'].is_anonymous())
        self.assertIn('Please enter a correct username and password',
                      response.content)

        response = self.client.post(self.login_url,
                                    {'username': self.user.username,
                                     'password': self.password})
        # correct credentials. redirecting
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('contacts_list'))
        self.assertEqual(response.context['user'], self.user)
        # logout
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('contacts_list'))
        self.assertTrue(response.context['user'].is_anonymous())
