# archivo forms.py
import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django_select2 import forms as s2forms

from catalog.models import BookInstance
from . import models

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

## Ahora el mismo formulario pero con ModelForm
class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
       data = self.cleaned_data['due_back']

       # Check if a date is not in the past.
       if data < datetime.date.today():
           raise ValidationError(_('Invalid date - renewal in past'))

       # Check if a date is in the allowed range (+4 weeks from today).
       if data > datetime.date.today() + datetime.timedelta(weeks=4):
           raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

       # Remember to always return the cleaned data.
       return data

    class Meta:
        model = BookInstance
        fields = ['due_back', 'status']
        labels = {'due_back': _('Renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}

## Crear un formulario de contacto
class ContactForm(forms.Form):
    ''' Contact form '''
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    from_email.widget.attrs.update({'class': 'form-control'})
    subject.widget.attrs.update({'class': 'form-control'})
    message.widget.attrs.update({'class': 'form-control'})

class AuthorWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        'first_name__icontains',
        'last_name__icontains',
    ]

class GenreWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        'name__icontains',
    ]

class LanguageWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        'name__icontains',
    ]

class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = '__all__'
        widgets = {
            'author': AuthorWidget,
            'genre': GenreWidget,
            'language': LanguageWidget
        }