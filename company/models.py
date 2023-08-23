from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    birthday = models.DateTimeField(verbose_name="Cumpleaños")
    country = models.CharField(max_length=50, verbose_name="Pais")
    indicative = models.CharField(max_length=3, verbose_name="Indicativo")
    contact = models.CharField(null=True, max_length=30, verbose_name="Contacto")
    gender = models.CharField(
        null=True,
        max_length=6,
        choices=[('Hombre','Hombre'),('Mujer','Mujer'),('Otros','Otros')]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="fecha actualizacion")

    def __str__(self):
        return self.user.username
    

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name = "Nombre")
    description = models.TextField(verbose_name="descripcion")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="fecha actualizacion")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
    
    def __str__(self):
        return self.name
    
class ProfileBussines(models.Model):
    name = models.CharField(max_length=100, verbose_name="nombre")
    user = models.ForeignKey(User, verbose_name="usuario" , on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name="categoria", on_delete=models.CASCADE)
    photo_portada = models.ImageField(upload_to="perfil_bussines", verbose_name="portada")
    photo_profile = models.ImageField(upload_to="perfil_bussines", verbose_name="perfil")
    description = models.TextField(max_length=500, verbose_name="descripcion")
    contact = models.CharField(max_length=50, verbose_name="contacto")
    email = models.EmailField(max_length=254, verbose_name="correo")
    facebook = models.CharField(max_length=300, null=True)
    instagram = models.CharField(max_length=300, null=True)
    whatsapp = models.CharField(max_length=300, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="fecha actualizacion")
    class Meta:
        verbose_name = "Perfil-Empresa"
        verbose_name_plural = "Perfiles-Empresas"

    
    def __str__(self):
        return self.name


class Catalogos(models.Model):
    name = models.CharField(max_length=100, verbose_name="nombre")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="fecha actualizacion")
    class Meta:
        verbose_name = "Catalogo"
        verbose_name_plural = "Catalogos"
    
    def __str__(self):
        return self.name