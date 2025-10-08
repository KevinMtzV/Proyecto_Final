# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Campana, Categoria

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Mantenemos los campos por defecto de Django: username, email y password
        fields = ('username', 'email')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: Podrías añadir personalización adicional al formulario aquí si fuera necesario
        pass

class CampanaForm(forms.ModelForm):
    """Formulario para la creación o edición de campañas."""
    class Meta:
        model = Campana
        fields = ['titulo', 'descripcion', 'fecha_limite', 'meta_monetaria', 'categoria']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()