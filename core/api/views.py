# core/api/views.py

from rest_framework import viewsets, filters, serializers
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Campana, Categoria, Donacion
from .serializers import CampanaSerializer, CategoriaSerializer, DonacionSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# --- ViewSet de Categorías (Solo Lectura) ---
class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """Permite listar y recuperar categorías de campañas."""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# --- ViewSet de Donaciones (Solo para crear) ---
# Usamos ModelViewSet para permitir POST (crear donación) y GET (listar donaciones)
class DonacionViewSet(viewsets.ModelViewSet):
    """Permite crear una donación. Listar todas las donaciones requiere autenticación."""
    queryset = Donacion.objects.all().order_by('-fecha_donacion')
    serializer_class = DonacionSerializer
    # Permite a cualquier usuario ver/listar, pero requiere autenticación para crear (lo controlaremos en perform_create)
    permission_classes = [IsAuthenticatedOrReadOnly] 
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['campana']
    ordering_fields = ['fecha_donacion', 'monto']
    pagination_class = None  # Deshabilitamos la paginación por defecto

    def filter_queryset(self, queryset):
        """Apply filtering and then limit"""
        # Primero aplicamos los filtros normales (incluyendo el filtro de campaña)
        queryset = super().filter_queryset(queryset)
        
        # Luego aplicamos el límite si existe
        limit = self.request.query_params.get('limit')
        if limit:
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except ValueError:
                pass
        
        return queryset
    
    def perform_create(self, serializer):
        # Valida que el usuario esté autenticado para hacer una donación.
        if self.request.user.is_authenticated:
            # Aquí se asocia la donación al usuario autenticado (donante)
            donacion = serializer.save(donante=self.request.user)
            
            # Lógica para actualizar el campo 'recaudado' de la Campaña (si aplica)
            campana = donacion.campana
            if donacion.tipo == 'M': # 'M'onetary (Monetaria)
                campana.recaudado = (campana.recaudado or 0) + donacion.monto
                campana.save(update_fields=['recaudado'])
        else:
            # Si se intenta donar sin autenticación, lanza un error
            raise serializers.ValidationError("Debe iniciar sesión para realizar una donación.")


# --- ViewSet de Campañas ---
class CampanaViewSet(viewsets.ModelViewSet):
    """Permite listar, crear, recuperar, actualizar y eliminar campañas."""
    queryset = Campana.objects.all().order_by('-fecha_creacion')
    serializer_class = CampanaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Permite a no autenticados ver, pero requiere login para modificar

    def perform_create(self, serializer):
        # Asigna el organizador automáticamente al usuario que hace la petición
        serializer.save(organizador=self.request.user)
    
    # Endpoint adicional para listar SÓLO las campañas del usuario autenticado
    @action(detail=False, methods=['get'], url_path='mis-campanas')
    def mis_campanas(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Autenticación requerida para ver sus campañas."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Filtra las campañas por el organizador actual
        campanas = self.get_queryset().filter(organizador=request.user)
        # Reutiliza el serializer de Campana
        serializer = self.get_serializer(campanas, many=True)
        return Response(serializer.data)