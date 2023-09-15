from django import forms
from django.core import validators
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from company.models import *
from .validators import MaxSizeFileValidator

class editCatalogoForm(forms.ModelForm):

    name = forms.CharField(
        max_length="40",
        required=True,
        validators = [
            validators.MaxLengthValidator(40,'Solo se admiten 40 caracteres')
        ]
    )

    description = forms.CharField(
        max_length="100",
        required=True,
        widget = forms.Textarea(

        )
    )

    class Meta:
        model = Catalogos
        fields = '__all__'
        exclude = ('user',)

class catalogForm(forms.Form):
    name = forms.CharField(
        max_length="40", 
        required=True,
        label="Nombre",
        widget= forms.TextInput(
            attrs={
                'placeholder':'Ingresa nombre de catalogo'
            }
        ),
        validators = [
            validators.MinLengthValidator(5, 'Nombre muy corto, porfavor ingresa un nombre coherente'),
            validators.MaxLengthValidator(50,'Nombre muy largo para tu catalogo, porfavor revisalo.')
        ]
    )

    photo_portada = forms.ImageField(label="Foto de portada",
    validators=[MaxSizeFileValidator(max_file_size=1)],
    required= False
    )

    description = forms.CharField(
        label = "Descripcion",
        max_length = 400,
        widget = forms.Textarea(
            attrs = {
                'placeholder': 'Descripcion de tu empresa'
            }
        ),
        validators = [
            validators.MinLengthValidator(10, 'Descripcion muy corta, proporciona mas informacion para que tus clientes te conozcan mejor.'),
            validators.MaxLengthValidator(150, 'Cantidad maxima de caracteres es de 150, porfavor reduce tu descripcion.')
        ]
    )


class eForm(forms.ModelForm):
    photo_portada = forms.ImageField(label='Foto portada', validators=[MaxSizeFileValidator(max_file_size=1)])
    bio = forms.CharField(
        widget = forms.Textarea(
            attrs={
                'placeholder':'Una corta presentacion de tu empresa'
            }
        )
    )

    class Meta:
        model = ProfileBussines
        fields = ('name','category','bio','photo_portada','photo_profile','description','contact','email','facebook','instagram','whatsapp')

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

    bio = forms.CharField(
        label = "Bio",
        max_length = 50,
        widget = forms.Textarea(
            attrs = {
                'placeholder': 'Presentacion corta de tu empresa'
            }
        ),
        validators = [
            validators.MinLengthValidator(5, 'Presentacion muy corta')
        ]
    )

    category = forms.ModelChoiceField(
        label = "Categoria",
        queryset=Category.objects.all()
    )


    photo_portada = forms.ImageField(
        label = "Foto portada",
        validators=[MaxSizeFileValidator(max_file_size=1)]
    )


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



    