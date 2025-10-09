# core/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_item(queryset, key):
    """
    Permite acceder a un elemento por su ID o clave dentro de un QuerySet.
    Se utiliza para buscar el nombre de la categoría por su ID.
    """
    try:
        # Busca el objeto dentro del QuerySet por la clave (ID)
        return queryset.get(id=key).nombre
    except:
        return ''