# archivo forms.py
import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Introduce una fecha entre hoy y 4 semanas(default 3).")

    def clean_renewal_date(self):
        '''Valida que la fecha no sea en el pasado y no mÃ¡s de 4 semanas en el futuro'''
        data = self.cleaned_data['renewal_date']

        # Comprueba que la fecha no sea en el pasado.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Comprueba que la fecha no sea más de 4 semanas en el futuro.
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Recuerda siempre devolver los datos limpios.
        return data 
