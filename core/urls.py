# core/urls.py

from django.urls import path
from . import views
from .views import CampanaCreateView

urlpatterns = [
    path('', views.home_view, name='home'),
    # URL de registro
    path('register/', views.register_view, name='register'), 
    path('campana/crear/', CampanaCreateView.as_view(), name='campana_crear'),
]