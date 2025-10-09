from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum

# --- Catálogos (Para cumplir con el Requisito 4) ---

class Categoria(models.Model):
    """Categoría de la donación/necesidad (e.g., Alimentos, Salud, Educación)."""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Categorías"
        
    def __str__(self):
        return self.nombre

# --- Entidades Principales (Requisito 1) ---

class Campana(models.Model):
    ORGANIZADOR = [
        ('ACT', 'Activa'),
        ('COM', 'Completada'),
        ('CAN', 'Cancelada'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField(default=timezone.now)
    meta_monetaria = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Nuevo campo para el monto recaudado
    recaudado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    organizador = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=3, choices=ORGANIZADOR, default='ACT')
    imagen = models.ImageField(upload_to='campana_pics/', 
                               null=True, blank=True, 
                               help_text="Imagen principal de la campaña.")

    def __str__(self):
        return self.titulo
    
    # Método para el porcentaje de meta completada
    @property
    def porcentaje_completado(self):
        if self.meta_monetaria > 0:
            return min(100, int((self.recaudado / self.meta_monetaria) * 100))
        return 0

# --- Nuevo Modelo para Donaciones (Requisito 2) ---

class Donacion(models.Model):
    TIPO_DONACION = [
        ('MON', 'Monetaria'),
        ('ART', 'Artículo'),
    ]
    
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, related_name='donaciones')
    # Permite donaciones anónimas si donante=None
    donante = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='donaciones_realizadas')
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    articulo_donado = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.CharField(max_length=3, choices=TIPO_DONACION)
    fecha_donacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donación {self.get_tipo_display()} a {self.campana.titulo}"