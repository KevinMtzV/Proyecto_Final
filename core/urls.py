# core/urls.py

from django.urls import path
from . import views
from .views import CampanaCreateView, CampanaListView, CampanaDetailView, donar_submit_view, UserDashboardView, CampanaUpdateView, UserPasswordChangeView

urlpatterns = [
    path('', views.home_view, name='home'),
    # URL de registro
    path('register/', views.register_view, name='register'), 
     # 1. Rutas de Campañas
    path('campana/crear/', CampanaCreateView.as_view(), name='campana_crear'), 
    path('campana/<int:pk>/editar/', CampanaUpdateView.as_view(), name='campana_editar'),
    path('campana/listado/', CampanaListView.as_view(), name='campana_listado'),
    path('campana/<int:pk>/', CampanaDetailView.as_view(), name='campana_detalle'),

     # 2. Ruta de Donación (POST)
    path('campana/<int:pk>/donar/', donar_submit_view, name='donar_submit'),

    # Ruta del Dashboard
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    # Alias semántico para Perfil apuntando al mismo dashboard
    path('perfil/', UserDashboardView.as_view(), name='perfil'),
    # Cambiar contraseña (vista personalizada sin crispy)
    path('perfil/cambiar-contrasena/', UserPasswordChangeView.as_view(), name='cambiar_contrasena'),
]