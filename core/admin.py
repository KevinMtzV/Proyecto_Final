from django.contrib import admin
from .models import Campana, Donacion, Categoria

# Podemos personalizar cómo se ven los modelos en el admin
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    
@admin.register(Campana)
class CampanaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'organizador', 'categoria', 'meta_monetaria', 'recaudado', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'categoria', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion')
    readonly_fields = ('recaudado',) # Para que el admin no pueda cambiar esto manualmente

@admin.register(Donacion)
class DonacionAdmin(admin.ModelAdmin):
    list_display = ('campana', 'donante', 'tipo', 'monto', 'fecha_donacion')
    list_filter = ('tipo', 'campana', 'fecha_donacion')
    search_fields = ('articulo_descripcion',)