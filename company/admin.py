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

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
admin.site.register(ProfileBussines, Bussines)


