from django import forms


class BotstrapDateInput(forms.DateInput):
    class Media:
        css : {
            all: ("http://cdnjs.cloudflare.com/ajax/libs/bootstrap-dateti\
                  mepicker/4.0.0/css/bootstrap-datetimepicker.min.css",)
        }
        js: {
            ('https://cdn.jsdelivr.net/bootstrap/3.3.6/js/bootstrap\
             .min.js', 'http://cdnjs.cloudflare.com/ajax/libs/bootstrap-datet\
             imepicker/4.0.0/js/bootstrap-datetimepicker.min.js')
        }
