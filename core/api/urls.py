# core/api/urls.py

from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, CampanaViewSet, DonacionViewSet


# Crea un router y registra nuestros ViewSets (Endpoints)
router = DefaultRouter()
router.register(r'campanas', CampanaViewSet)
router.register(r'donaciones', DonacionViewSet)
router.register(r'categorias', CategoriaViewSet)

# Las URLs generadas por el router se incluyen directamente en urlpatterns
urlpatterns = router.urls