from django.contrib.auth.models import User
from django.core.validators import validate_integer
from django.forms import ModelForm, CheckboxInput
from django.contrib.auth.forms import UserCreationForm
from models import Paciente

__author__ = 'Jesus'

from django import forms


class Login(UserCreationForm):
    class Meta:
        model = User
        fields = {'username', 'password'}
        # Username = forms.CharField(label='Usuario:', max_length=10)
        # Password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        # self.fields['username'].widget.attrs.update({'class': 'form-control'})
        # self.fields['password'].widget.attrs.update({'class': 'form-control'})


class CreateUser(ModelForm):
    class Meta:
        model = User
        fields = {'username', 'password', 'first_name', 'last_name', 'email', 'is_superuser'}
        widgets = {'is_superuser': CheckboxInput,
                   'password': forms.PasswordInput}
        help_texts = {
            'username': None,
            'is_superuser': "Designa si el usuario sera adminsitrador o no"
        }


class CreatePaciente(ModelForm):

    class Meta:
        model = Paciente
        fields = { 'Dni_P','Nombre_P', 'Apellido_P','Fecha_Ingreso'}
        widgets = {'Fecha_Ingreso':forms.SelectDateWidget(years=('2016','2017','2018','2019','2020'))
        }
        labels = {
            'Dni_P': "Dni",
            'Nombre_P': "Nombre del Paciente",
            'Apellido_P': "Apellido del Paciente",
        }

    def clean_dni(self,dni):
        if dni.isdigit():
            if len(dni) != 8:
                raise forms.ValidationError("El Dni debe contener 8 caracteres numericos")
        else:
            raise forms.ValidationError("El Dni debe contener 8 caracteres numericos")
        return dni
