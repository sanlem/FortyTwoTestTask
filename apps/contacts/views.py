from django.shortcuts import render
from apps.contacts.models import Contacts
from apps.contacts.forms import ContactsEditForm
from django.views.generic import UpdateView
from django.http import HttpResponse
from django.core.urlresolvers import reverse


def contacts_list(request):
    contacts = Contacts.objects.last()
    return render(request, 'contacts.html', {"contacts": contacts})


class ContactsUpdateView(UpdateView):
    form_class = ContactsEditForm
    model = Contacts
    template_name = 'edit.html'

    def get_success_url(self):
        return reverse('contacts_list')

    def get_object(self):
        return Contacts.objects.last()

    def post(self, request, *args, **kwargs):
        if not self.get_object():
            return HttpResponse(status=400)
        return super(ContactsUpdateView, self).post(request, *args, **kwargs)
