from django.shortcuts import render
from apps.contacts.models import Contacts
from apps.contacts.forms import ContactsEditForm
from django.views.generic import UpdateView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from apps.contacts import signals


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

    def get_object(self):
        return Contacts.objects.last()

    def post(self, request, *args, **kwargs):
        if not self.get_object():
            return HttpResponse(status=400)
        return super(ContactsUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Saved successfully.')
        return self.render_to_response(self.get_context_data(form=form))
