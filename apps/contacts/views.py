from django.shortcuts import render
from apps.contacts.models import Contacts
from apps.contacts.forms import ContactsEditForm
from django.views.generic import UpdateView
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def contacts_list(request):
    contacts = Contacts.objects.last()
    return render(request, 'contacts.html', {"contacts": contacts})


class ContactsUpdateView(UpdateView):
    form_class = ContactsEditForm
    model = Contacts
    template_name = 'edit.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, *args, **kwargs):
        return super(ContactsUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('contacts_list')

    def get_object(self):
        return Contacts.objects.last()

    def post(self, request, *args, **kwargs):
        if not self.get_object():
            return HttpResponse(status=400)
        return super(ContactsUpdateView, self).post(request, *args, **kwargs)
