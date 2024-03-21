from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Temario)
class Temario(admin.ModelAdmin):
    list_display = ('NomTemario', 'NumPaginas', 'TemVisible','Archivo', 'NomUsuario', 'IdOposicion')
    search_fields = ('NomTemario'),

@admin.register(models.Oposicion)
class Oposicion(admin.ModelAdmin):
    list_display = ('NomOposicion', 'OpoVisible')
    search_fields = ('NomOposicion'),

@admin.register(models.Prueba)
class Prueba(admin.ModelAdmin):
    list_display = ('NomPrueba', 'NumPreguntas', 'PruVisible')
    search_fields = ('NomPrueba'),

@admin.register(models.Progreso)
class Progreso(admin.ModelAdmin):
    list_display = ('id', 'Nota', 'PregAcertadas', 'PregFalladas','PregBlanco','Tiempo','IdPrueba')
    search_fields = ('id'),

@admin.register(models.Formado_por)
class Formado_por(admin.ModelAdmin):
    list_display = ('IdTemario','IdPrueba')
    