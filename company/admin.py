from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'

class CustomizedUserAdmin (UserAdmin):
    inlines = (AccountInline,)

class Bussines(admin.ModelAdmin):
    list_display = ('name','category','email')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description','created_at')

class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name','photo_portada','description','category_id','profile_id','user_id','created_at')
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id_product','name_product','quantities','price','photo_product1','category_id','profile_id','user_id')

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
admin.site.register(ProfileBussines,Bussines)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Catalogos,CatalogAdmin)
admin.site.register(Products,ProductAdmin)


