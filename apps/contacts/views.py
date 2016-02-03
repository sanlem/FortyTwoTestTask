from django.shortcuts import render
from apps.contacts.models import Contacts


def contacts_list(request):
    contacts = Contacts.objects.last()
    return render(request, 'contacts.html', {"contacts": contacts})

def contacts_edit(request):
    return render(request, 'edit.html', {})
