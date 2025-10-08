# core/views.py

from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Campana # Importamos para mostrar las campañas

def home_view(request):
    # Obtener un listado de campañas activas (Requisito 12 - Búsqueda/Filtrado Básico)
    campanas_activas = Campana.objects.filter(estado='ACT').order_by('-fecha_creacion')[:6]
    
    context = {
        'campanas': campanas_activas
    }
    return render(request, 'core/home.html', context)