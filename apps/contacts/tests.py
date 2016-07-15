from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from apps.contacts.models import Contacts, ChangeEntry
from datetime import datetime, date
from apps.contacts.forms import ContactsEditForm
from django.contrib.auth.models import User
from django.utils.six import StringIO
from django.core.management import call_command
from django.template import Template, Context


class TestContactsView(TestCase):

    fixtures = ['data.json']

    def setUp(self):
        # create contacts object
        self.contacts = Contacts.objects.last()
        # remember client
        self.client = Client()
        # remember url
        self.url = reverse("contacts_list")

    def test_contacts_list(self):
        """ testing contacts list view """
        response = self.client.get(self.url)
        # checking response's status code
        self.assertEqual(response.status_code, 200)
        # check if the proper template was used
        self.assertTemplateUsed(response, 'contacts.html')
        # check if we have correct name in content
        self.assertIn(self.contacts.name, response.content)
        # check if we have "Bio:" label in content
        self.assertIn("Bio:", response.content)
        # check if we have br tag in conent
        self.assertIn("br", response.content)
        # ensure view had only returned Contacts
        self.assertTrue(isinstance(response.context['contacts'], Contacts))
        # check if we have admin edit link
        edit_url = reverse('admin:contacts_contacts_change',
                           args=[self.contacts.id])
        self.assertIn(edit_url, response.content)
        # if there are more than 1 contacts, should return the first
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
        self.assertEqual(response.context['contacts'].id, 1)
        # should render 'No contacts.' if aren't any
        Contacts.objects.all().delete()
        response = self.client.get(self.url)
        self.assertIn('No contacts.', response.content)


class TestContactsModel(TestCase):

    fixtures = ['data.json']

    def test_unicode(self):
        """ only custom methods need to be tested """
        contacts = Contacts.objects.last()
        self.assertEqual(unicode(contacts), u"Myname Mylastname's contacts")

update_dict = {
    'name': 'Pavlo',
    'lastname': 'Samboruk',
    'email': 'asd@ex.com',
    'date_of_birth': date.today()
}


class TestContactsEditView(TestCase):

    fixtures = ['data.json']

    def setUp(self):
        # create contacts object
        self.contacts = Contacts.objects.last()
        # remember client
        self.client = Client()
        self.client.login(username='admin', password='admin')
        # remember url
        self.url = reverse("contacts_edit")
        # remember image
        self.image = open('./assets/test_image.png')

    def test_login_required(self):
        """ page requires login """
        self.client.logout()
        response = self.client.get(self.url)
        # not authenticated
        url = reverse('login') + '?next=/edit/'
        self.assertRedirects(response, url, status_code=302)
        self.client.login(username='admin', password='admin')
        # authenticated now
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_contacts_edit_page(self):
        """ test contacts' edition page content """
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)
        # check if the proper template was used
        self.assertTemplateUsed(response, 'edit.html')
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

    def test_valid_data(self):
        """ test contact's edition """
        response = self.client.post(self.url, update_dict)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Saved successfully', response.content)
        # ensure the name is changed
        self.assertEqual(Contacts.objects.get(pk=1).name, 'Pavlo')

    def test_more_than_one_object(self):
        """ should edit the first object """
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
        # ensure view edits the first object
        self.client.post(self.url, params)
        self.assertEqual(Contacts.objects.get(pk=1).name, 'Vitaliy')
        self.assertEqual(Contacts.objects.get(pk=2).name, 'Myname')

    def test_invalid_data(self):
        """ invalid data """
        params = update_dict.copy()
        params['name'] = ''
        params['date_of_birth'] = 'azaza'
        params['email'] = 'azaza'
        response = self.client.post(self.url, params)
        self.assertIn('This field is required.', response.content)
        self.assertIn('Enter a valid date.', response.content)
        self.assertIn('Enter a valid email address.', response.content)
        # ensure object didn't changed
        self.assertEqual(Contacts.objects.get(pk=1).name, 'Myname')

    def test_no_contacts(self):
        """ if there are no contacts """
        Contacts.objects.all().delete()
        # should render 'Can't edit. No contacts exist.'
        response = self.client.get(self.url)
        self.assertIn("Can't edit. No contacts exist.", response.content)
        # should return 400 status code for post requests if no objects
        response = self.client.post(self.url, {'name': 'Vitaliy'})
        self.assertEqual(response.status_code, 400)

    def test_image_upload(self):
        """ some tests for image uploading """
        params = update_dict.copy()
        params.update({'image': self.image})
        response = self.client.post(reverse('contacts_edit'), params)
        contacts = Contacts.objects.last()
        self.assertEqual(response.status_code, 200)
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
        # check if the proper template was used
        self.assertTemplateUsed(response, 'login.html')
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


class TestCommand(TestCase):

    def setUp(self):
        for i in range(4):
            u = User(username='usr' + str(i))
            u.save()

        c = Contacts(**update_dict)
        c.save()

        client = Client()
        for i in range(3):
            client.get(reverse('login'))

    def test_command(self):
        """ test of command's output """
        out = StringIO()
        err = StringIO()
        call_command('models_info', stdout=out, stderr=err)

        result_out = out.getvalue()
        result_err = err.getvalue()
        self.assertIn('user in database: 4', result_out)
        self.assertIn('error: user in database: 4', result_err)
        self.assertIn('contacts in database: 1', result_out)
        self.assertIn('error: contacts in database: 1', result_err)
        self.assertIn('requestentry in database: 3', result_out)
        self.assertIn('error: requestentry in database: 3', result_err)


class TestSignalProcessor(TestCase):

    fixtures = ['data.json']

    def setUp(self):
        self.user = User.objects.last()

    def test_creation(self):
        """ creating some objects and checking theirs ChangeEntries. """
        # user from fixture was created
        change = ChangeEntry.objects.last()
        self.assertEqual(change.model_name, 'User')
        self.assertEqual(change.action, 'created')
        self.assertEqual(change.instance_id, self.user.id)

    def test_updation(self):
        """ test for updating """
        self.user.set_password('bla')
        self.user.save()
        # test update
        change = ChangeEntry.objects.last()
        self.assertEqual(change.action, 'updated')
        self.assertEqual(change.instance_id, self.user.id)
        counter = ChangeEntry.objects.filter(model_name='User').count()
        self.assertEqual(counter, 2)

    def test_deletion(self):
        """ test for deleting """
        # remember user's id before deletion
        deleted_id = self.user.id
        self.user.delete()
        change = ChangeEntry.objects.last()
        self.assertEqual(change.action, 'deleted')
        self.assertEqual(change.instance_id, deleted_id)
        counter = ChangeEntry.objects.filter(model_name='User').count()
        self.assertEqual(counter, 2)


class TestTemplateTags(TestCase):

    def test_edit_link(self):
        """ test edit_link tag. """
        c = Contacts(**update_dict)
        template = Template(
            "{% load link %}"
            "{% edit_link obj %}"
        )
        out = template.render(Context({'obj': c}))
        edit_url = reverse('admin:contacts_contacts_change',
                           args=[c.id])
        self.assertIn(edit_url, out)
        # nothing should be rendered if no object passed
        out = template.render(Context({}))
        self.assertEqual(out, '')
