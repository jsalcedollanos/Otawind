from django import forms
from django.core import validators
from .models import ProfileBussines
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from company.models import *


class Form(forms.Form):
    name = forms.CharField(
        label = "Nombre",
        max_length = 40,
        required = True,
        widget = forms.TextInput(
            attrs={
                'placeholder':'Tu empresa'
            }
        ),
        validators = [
            validators.MinLengthValidator(4, 'Nombre demasiado corto')
        ]
    )

    category = forms.ModelChoiceField(
        label = "Categoria",
        queryset=Category.objects.all()
    )


    photo_portada = forms.ImageField(label = "Foto portada")
    photo_profile = forms.ImageField(label = "Foto perfil")
    description = forms.CharField(
        label = "Descripcion",
        max_length = 400,
        widget = forms.Textarea(
            attrs = {
                'placeholder': 'Descripcion de tu empresa'
            }
        ),
        validators = [
            validators.MinLengthValidator(10, 'Descripcion muy corta, proporciona mas informacion para que tus clientes te conozcan mejor')
        ]
    )

    contact = forms.CharField(
        label = "Telefono",
        max_length = 15,
        required = True,
        widget = forms.TextInput(
            attrs = {
                'placeholder':'Telefono de tu empresa'
            }
        ),
        validators = [
            validators.MaxLengthValidator(15,'El numero de contacto que proporsionaste es muy largo, revisalo de nuevo')
        ]
    )

    email = forms.EmailField(
        label="Correo", 
        max_length= 80, 
        required = True,
        widget = forms.EmailInput(
            attrs = {
                'placeholder':'Tu correo corporativo'
            }
        ),
        validators = [
            validators.MinLengthValidator(10, 'El correo proporcionado es muy corto'),
            validators.MaxLengthValidator(80, 'El correo proporsionado es demasiado largo revisalo porfavor')
        ]
    )

    facebook = forms.CharField(
        label = "Facebook",
        required = False,
        max_length = 255,
        widget = forms.TextInput(
            attrs = {
                'placeholder':'Link de Facebook'
            }
        )
    )

    instagram = forms.CharField(
        label = "Instagram",
        required = False,
        max_length = 255,
        widget = forms.TextInput(
            attrs = {
                'placeholder':'Link de Instagram'
            }
        )
    )

    whatsapp = forms.CharField(
        label = "Whatsapp",
        required = False,
        max_length = 255,
        widget = forms.TextInput(
            attrs = {
                'placeholder':'Link de Whatsapp'
            }
        )
    )

    


class login(UserCreationForm):
    class Meta:
        model: User
        fields = ['email','password1']

class formAccount(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
    