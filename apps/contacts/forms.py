from django import forms
from apps.contacts.models import Contacts


class BootstrapDateInput(forms.DateInput):
    class Media:
        css = {
            all: ('http://cdnjs.cloudflare.com/ajax/libs/bootstrap-' +
                  'datetimepicker/4.0.0/css/bootstrap-datetimepicker.min.css')
        }
        js = ('https://cdn.jsdelivr.net/bootstrap/3.3.6/js/bootstrap.min.js',
              'http://cdnjs.cloudflare.com/ajax/libs/bootstrap-' +
              'datetimepicker/4.0.0/js/bootstrap-datetimepicker.min.js',
              'js/initDateInput.js')


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

        field = self.fields.get('date_of_birth')
        field.widget.attrs['class'] += ' datepicker'
