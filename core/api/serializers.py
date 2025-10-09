# core/api/serializers.py

from rest_framework import serializers
from core.models import Categoria, Campana, Donacion

# --- Categoria Serializer (Lectura de catálogo) ---
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id', 'nombre')

# --- Donacion Serializer (Solo para mostrar en el detalle de Campaña) ---
class DonacionSerializer(serializers.ModelSerializer):
    # Campos de solo lectura para el donante y la campaña
    donante_username = serializers.ReadOnlyField(source='donante.username') 
    campana_titulo = serializers.ReadOnlyField(source='campana.titulo')
    
    class Meta:
        model = Donacion
        # Exponemos todos los campos, pero solo algunos serán editables/creables
        fields = ('id', 'donante_username', 'campana_titulo', 'tipo', 'monto', 'articulo_donado', 'fecha_donacion')
        read_only_fields = ('fecha_donacion',) # La fecha se establece automáticamente

# --- Campana Serializer (La entidad principal) ---
class CampanaSerializer(serializers.ModelSerializer):
    # Campos de relaciones
    organizador_username = serializers.ReadOnlyField(source='organizador.username')
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    
    # Opcional: Mostrar las últimas 5 donaciones en el detalle de la campaña
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
            'organizador_username', # Vía ReadOnlyField
            'categoria_nombre',     # Vía ReadOnlyField
            'categoria',            # Para la escritura (POST/PUT)
            'ultimas_donaciones'
        )
        read_only_fields = ('recaudado', 'organizador',) # No se puede editar manualmente
        
    def get_ultimas_donaciones(self, obj):
        """Método para obtener y serializar las donaciones de una campaña."""
        donaciones = obj.donacion_set.all().order_by('-fecha_donacion')[:5]
        # Usamos DonacionSerializer para serializar estas donaciones
        return DonacionSerializer(donaciones, many=True).data