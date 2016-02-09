from django import forms
from apps.contacts.models import Contacts
from apps.contacts.widgets import BootstrapDateInput


class ContactsEditForm(forms.ModelForm):
    class Meta:
        model = Contacts
        widgets = {
            'date_of_birth': BootstrapDateInput(),
            'other_contacts': forms.Textarea(attrs={'rows': 3}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(ContactsEditForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'class': 'form-control'
                })

        # we will init as datepicker field found by this class
        field = self.fields.get('date_of_birth')
        field.widget.attrs['class'] += ' datepicker'
        # delete form-control class from ImageField widget
        field = self.fields.get('image')
        field.widget.attrs.pop('class')
