# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Campana, Categoria, Donacion
from django import forms

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


# formulario para Donacion
class DonacionForm(forms.ModelForm):
    """Formulario para realizar una donación."""
    monto = forms.DecimalField(
        label='Monto a Donar ($)', 
        required=False, 
        min_value=1.00,
        widget=forms.NumberInput(attrs={'placeholder': 'Monto (solo monetaria)'})
    )
    articulo_donado = forms.CharField(
        label='Descripción del Artículo', 
        max_length=255, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Descripción (solo artículos)'})
    )
    
    class Meta:
        model = Donacion
        # 'campana', 'donante', 'fecha_donacion' se llenan en la vista
        fields = ['tipo', 'monto', 'articulo_donado']
        
    def clean(self):
        """Validación para asegurar que se ingresa un monto O un artículo."""
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        monto = cleaned_data.get('monto')
        articulo = cleaned_data.get('articulo_donado')

        if tipo == 'MON' and not monto:
            self.add_error('monto', "Debe ingresar un monto para una donación monetaria.")
        if tipo == 'ART' and not articulo:
            self.add_error('articulo_donado', "Debe describir el artículo donado.")
        
        return cleaned_data