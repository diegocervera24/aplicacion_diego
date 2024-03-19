from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.User)
class User(admin.ModelAdmin):
    list_display = ('username', 'email', 'nombre', 'password')
    search_fields = ('username'),

# Register your models here.
