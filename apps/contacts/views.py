from django.shortcuts import render
import datetime


def contacts_list(request):
    contacts = [{'name': "Myname",
                 'lastname': "Mylastname",
                 'email': "myemail",
                 'date_of_birth': datetime.datetime.today(),
                 'jabber_id': "myjabber",
                 'skype_login': "myskype",
                 'bio': "bio!",
                 'other_contacts': "blabla"}]
    return render(request, 'contacts.html', {"contacts": contacts})
