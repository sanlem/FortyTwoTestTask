from django.shortcuts import render
from django.core.management import call_command
from apps.contacts.models import Contacts


def contacts_list(request):
    call_command('loaddata', 'contacts.json', verbosity=0)
    contacts = Contacts.objects.all()[:3]
    return render(request, 'contacts.html', {"contacts": contacts})
