# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Campana, Categoria, Donacion

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
        fields = ['titulo', 'descripcion', 'fecha_limite', 'meta_monetaria', 'categoria', 'imagen']
        
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


class CustomPasswordChangeForm(PasswordChangeForm):
    """Formulario personalizado para cambiar contraseña con textos en español."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personaliza etiquetas, ayudas y placeholders
        self.fields['old_password'].label = 'Contraseña actual'
        self.fields['old_password'].widget.attrs.update({
            'placeholder': 'Ingresa tu contraseña actual'
        })

        self.fields['new_password1'].label = 'Nueva contraseña'
        self.fields['new_password1'].help_text = (
            'Debe tener al menos 8 caracteres, no puede parecerse demasiado a tu información personal, '
            'no puede ser una contraseña común ni completamente numérica.'
        )
        self.fields['new_password1'].widget.attrs.update({
            'placeholder': 'Elige una nueva contraseña segura'
        })

        self.fields['new_password2'].label = 'Confirmar nueva contraseña'
        self.fields['new_password2'].widget.attrs.update({
            'placeholder': 'Repite la nueva contraseña'
        })

        # Mensajes de error personalizados
        self.error_messages['password_mismatch'] = 'Las contraseñas no coinciden.'
        self.error_messages['password_incorrect'] = 'La contraseña actual no es correcta.'