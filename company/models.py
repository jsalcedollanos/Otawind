from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Color(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="fecha actualizacion")

class Account(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    photo_profile = models.ImageField(upload_to="perfil_bussines", verbose_name="perfil", null=True)
    birthday = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="Cumpleaños")
    country = models.CharField(max_length=50, verbose_name='Pais')
    city = models.CharField(max_length=50, verbose_name='Ciudad')
    bio = models.TextField(max_length=50, null=True)
    email = models.EmailField(max_length=254, verbose_name='Correo')
    facebook = models.CharField(max_length=300, null=True)
    instagram = models.CharField(max_length=300, null=True)
    whatsapp = models.CharField(max_length=300, null=True)
    indicative = models.CharField(max_length=3, verbose_name="Indicativo")
    contact = models.CharField(null=True, max_length=30, verbose_name="Contacto")
    gender = models.CharField(
        verbose_name = 'Genero',
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
    type_categorie = models.CharField(max_length=15, verbose_name= "tipo_categoria")
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
    bio = models.TextField(max_length=50, null=True)
    category = models.ForeignKey(Category, verbose_name="categoria", on_delete=models.CASCADE, default=True)
    photo_portada = models.ImageField(upload_to="perfil_bussines", verbose_name="portada", null=True)
    photo_profile = models.ImageField(upload_to="perfil_bussines", verbose_name="perfil", null=True)
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
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(ProfileBussines, verbose_name="perfil", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=40, verbose_name="nombre")
    category = models.ForeignKey(Category, verbose_name="categoria", on_delete=models.CASCADE)
    type_catalog = models.CharField(
        max_length = 10,
        verbose_name = 'Tipo catalogo',
        choices = [('Servicios','Servicios'),('Productos','Productos')]
    )
    photo_portada = models.ImageField(upload_to="catalogo", verbose_name="portada", null=True)
    description = models.TextField(max_length=2000, null=True, verbose_name="descripcion")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="fecha actualizacion")
    class Meta:
        verbose_name = "Catalogo"
        verbose_name_plural = "Catalogos"
    
    def __str__(self):
        return self.name
    
class Products(models.Model):
    name_product = models.CharField(max_length=100, verbose_name="Nombre")
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    catalog = models.ForeignKey(Catalogos, verbose_name="catalogo", on_delete=models.CASCADE)
    id_product = models.CharField(max_length=10, unique=True, verbose_name="id_producto")
    profile = models.ForeignKey(ProfileBussines, verbose_name="Perfil", on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, verbose_name="Categoria", on_delete=models.CASCADE, default="None")
    quantities = models.CharField(max_length=4, verbose_name="Cantidades", null=True)
    brand = models.CharField(max_length=30, verbose_name="Marca")
    status = models.CharField(max_length=20, verbose_name="estado", default='Activo')
    color = models.CharField(max_length=50, null=True)
    valoration = models.CharField(verbose_name="Valoracion", max_length=3, default='3.5')
    price = models.IntegerField(verbose_name="precio")
    price_promo = models.IntegerField(verbose_name='promocion', default="0")
    description = models.TextField(max_length=1000, verbose_name="descripcion", default="Descripcion del producto")
    photo_product1 = models.ImageField(upload_to="productos", verbose_name="foto_producto1")
    photo_product2 = models.ImageField(upload_to="productos", verbose_name="foto_producto2", null=True)
    photo_product3 = models.ImageField(upload_to="productos", verbose_name="foto_producto3", null=True)
    photo_product4 = models.ImageField(upload_to="productos", verbose_name="foto_producto4", null=True)
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    
    def __str__(self):
        return self.name_product
    

class Services(models.Model):
    name_service = models.CharField(max_length=40, verbose_name="Nombre")
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    catalog = models.ForeignKey(Catalogos, verbose_name="catalogo", on_delete=models.CASCADE)
    id_service = models.CharField(max_length=10, unique=True, verbose_name="id_servicio")
    profile = models.ForeignKey(ProfileBussines, verbose_name="Perfil", on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, verbose_name="Categoria", on_delete=models.CASCADE, default="None")
    valoration = models.CharField(verbose_name="Valoracion", max_length=3, default='3.5')
    status = models.CharField(max_length=20, verbose_name="estado", default='Activo')
    price = models.IntegerField(verbose_name="precio")
    price_promo = models.IntegerField(verbose_name='promocion', default="0")
    description = models.TextField(max_length=1000, verbose_name="descripcion", default="Descripcion del servicio")
    photo_service1 = models.ImageField(upload_to="servicios", verbose_name="foto_servicio1")
    photo_service2 = models.ImageField(upload_to="servicios", verbose_name="foto_servicio2", null=True)
    photo_service3 = models.ImageField(upload_to="servicios", verbose_name="foto_servicio3", null=True)
    photo_service4 = models.ImageField(upload_to="servicios", verbose_name="foto_servicio4", null=True)
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
    
    def __str__(self):
        return self.name_service