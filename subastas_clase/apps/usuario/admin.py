from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'first_name', 'last_name', 'documento_identidad', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('documento_identidad', 'domicilio')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('documento_identidad', 'domicilio')}),
    )

admin.site.register(Usuario, UsuarioAdmin)