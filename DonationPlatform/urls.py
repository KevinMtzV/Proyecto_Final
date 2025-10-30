# DonationPlatform/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 
from core.api import urls as api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    # 1. Rutas de autenticación de Django (Login, Logout, Password Reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    # 2. Rutas de la aplicación 'core'
    path('', include('core.urls')),
    # RUTA PARA LA WEB API (API REST)
    path('api/v1/', include((api_urls, 'api'))),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)