# core/views.py

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin # Para vistas basadas en clases
from .forms import CustomUserCreationForm, CampanaForm # Importamos el nuevo formulario
from .models import Campana 

def home_view(request):
    # Obtener un listado de campañas activas (Requisito 12 - Búsqueda/Filtrado Básico)
    campanas_activas = Campana.objects.filter(estado='ACT').order_by('-fecha_creacion')[:6]
    
    context = {
        'campanas': campanas_activas
    }
    return render(request, 'core/home.html', context)

# Nueva Vista para el Registro
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Opcional: Inicia sesión al usuario después del registro
            login(request, user) 
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/register.html', {'form': form})


# Nueva Vista para Crear Campaña (Usa CreateView y LoginRequiredMixin)
class CampanaCreateView(LoginRequiredMixin, CreateView):
    model = Campana
    form_class = CampanaForm
    template_name = 'core/campana_form.html'
    success_url = reverse_lazy('home') # Redirige a la página de inicio al guardar

    def form_valid(self, form):
        # Asigna automáticamente el usuario logueado como organizador (Requisito 3)
        form.instance.organizador = self.request.user 
        return super().form_valid(form)

