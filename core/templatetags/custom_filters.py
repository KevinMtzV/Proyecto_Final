# core/templatetags/custom_filters.py

from django import template
from core.models import Categoria # <--- IMPORTACIÓN NECESARIA

register = template.Library()

@register.filter
def get_item(queryset, key):
    """
    Busca el nombre de una categoría específica por su ID (key)
    dentro del queryset de categorías.
    """
    if not key:
        return ''
        
    try:
        # Intentamos obtener la categoría del QuerySet por su clave primaria (pk)
        # Esto es más eficiente si el QuerySet ya fue pasado desde la vista.
        return queryset.get(pk=key).nombre
    except AttributeError:
        # Si el primer argumento no es un QuerySet (por ejemplo, es un diccionario), intentamos la búsqueda directa.
        if isinstance(queryset, dict):
             return queryset.get(key, '')
        
    except Categoria.DoesNotExist:
        # Esto maneja el caso donde el ID existe en la URL pero no en la base de datos.
        return "Categoría no encontrada"
        
    except Exception:
        # Fallback para cualquier otro error
        return ''