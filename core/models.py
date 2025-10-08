from django.db import models
from django.contrib.auth.models import User

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
    """Una campaña para recaudar donaciones para una necesidad específica."""
    
    ESTADOS = [
        ('ACT', 'Activa'),
        ('PAU', 'Pausada'),
        ('FIN', 'Finalizada'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField(null=True, blank=True)
    meta_monetaria = models.DecimalField(max_digits=10, decimal_places=2, 
                                         default=0, help_text="Meta en dinero (0 si es de artículos)")
    recaudado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    organizador = models.ForeignKey(User, on_delete=models.CASCADE) # El usuario que crea la campaña
    estado = models.CharField(max_length=3, choices=ESTADOS, default='ACT')

    class Meta:
        verbose_name_plural = "Campañas"
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return self.titulo
    
    @property
    def porcentaje_completado(self):
        if self.meta_monetaria > 0:
            return min(100, int((self.recaudado / self.meta_monetaria) * 100))
        return 0

class Donacion(models.Model):
    """Registro de una donación monetaria o de artículos."""
    
    TIPO_DONACION = [
        ('MON', 'Monetaria'),
        ('ART', 'Artículo/Especie'),
    ]
    
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE)
    donante = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                 blank=True, related_name='donaciones_realizadas') # Puede ser anónimo
    tipo = models.CharField(max_length=3, choices=TIPO_DONACION, default='MON')
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    articulo_descripcion = models.CharField(max_length=255, blank=True, 
                                            help_text="Descripción del artículo si no es monetaria")
    fecha_donacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Donaciones"
        ordering = ['-fecha_donacion']
        
    def __str__(self):
        return f"Donación a {self.campana.titulo} por {self.monto or self.articulo_descripcion}"