from django.shortcuts import render
from apps.contacts.models import Contacts


def contacts_list(request):
    contacts = Contacts.objects.all()[:3]
    return render(request, 'contacts.html', {"contacts": contacts})
