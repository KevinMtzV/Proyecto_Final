# core/api/serializers.py

from rest_framework import serializers
from core.models import Categoria, Campana, Donacion
from django.contrib.auth.models import User

# --- Usuario Serializer (Para incluir info completa del usuario) ---
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')

# --- Categoria Serializer (Lectura de catálogo) ---
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id', 'nombre')

# --- Donacion Serializer (Solo para mostrar en el detalle de Campaña) ---
class DonacionSerializer(serializers.ModelSerializer):
    # Objetos completos anidados (solo lectura)
    donante = UsuarioSerializer(read_only=True)
    campana = serializers.SerializerMethodField()
    
    # Campos simples para compatibilidad (opcional)
    donante_username = serializers.ReadOnlyField(source='donante.username') 
    campana_titulo = serializers.ReadOnlyField(source='campana.titulo')
    
    class Meta:
        model = Donacion
        # Exponemos todos los campos, incluidos los objetos anidados
        fields = (
            'id', 
            'donante',              # Objeto completo del usuario
            'donante_username',     # Solo el username
            'campana',              # Objeto completo de la campaña
            'campana_titulo',       # Solo el título 
            'tipo', 
            'monto', 
            'articulo_donado', 
            'fecha_donacion'
        )
        read_only_fields = ('fecha_donacion',)
    
    def get_campana(self, obj):
        """Serializa la campaña relacionada sin donaciones para evitar recursión."""
        from .serializers import CampanaSimpleSerializer
        return CampanaSimpleSerializer(obj.campana).data

# --- Campana Simple Serializer (Sin donaciones para evitar recursión) ---
class CampanaSimpleSerializer(serializers.ModelSerializer):
    organizador = UsuarioSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    
    class Meta:
        model = Campana
        fields = (
            'id', 
            'titulo', 
            'descripcion', 
            'fecha_creacion', 
            'fecha_limite', 
            'meta_monetaria', 
            'recaudado', 
            'estado', 
            'imagen',
            'organizador',  # Objeto completo del organizador
            'categoria'     # Objeto completo de la categoría
        )

# --- Campana Serializer (La entidad principal con donaciones) ---
class CampanaSerializer(serializers.ModelSerializer):
    # Objetos completos anidados (solo lectura)
    organizador = UsuarioSerializer(read_only=True)
    categoria_obj = CategoriaSerializer(source='categoria', read_only=True)
    
    # Campos simples para compatibilidad
    organizador_username = serializers.ReadOnlyField(source='organizador.username')
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    
    # Mostrar las últimas 5 donaciones en el detalle de la campaña
    ultimas_donaciones = serializers.SerializerMethodField()

    class Meta:
        model = Campana
        fields = (
            'id', 
            'titulo', 
            'descripcion', 
            'fecha_creacion', 
            'fecha_limite', 
            'meta_monetaria', 
            'recaudado', 
            'estado', 
            'imagen',
            'organizador',          # Objeto completo del organizador
            'organizador_username', # Solo username
            'categoria_obj',        # Objeto completo de categoría
            'categoria_nombre',     # Solo nombre
            'categoria',            # ID para escritura
            'ultimas_donaciones'
        )
        read_only_fields = ('recaudado', 'organizador',)
        
    def get_ultimas_donaciones(self, obj):
        """Método para obtener y serializar las donaciones de una campaña."""
        donaciones = obj.donaciones.all().order_by('-fecha_donacion')[:5]
        # Usamos DonacionSerializer para serializar estas donaciones
        return DonacionSerializer(donaciones, many=True).data