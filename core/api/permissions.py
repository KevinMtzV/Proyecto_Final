# core/api/permissions.py

from rest_framework import permissions


class IsOrganizadorOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado que permite:
    - Cualquiera puede ver (GET, HEAD, OPTIONS)
    - Solo el organizador de la campaña puede modificar o eliminar (PUT, PATCH, DELETE)
    """
    
    def has_permission(self, request, view):
        # Permitir métodos de solo lectura a cualquiera
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Para métodos de escritura, el usuario debe estar autenticado
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Permitir lectura a cualquiera
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Para modificar o eliminar, el usuario debe ser el organizador
        return obj.organizador == request.user
