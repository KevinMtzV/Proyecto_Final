# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import TemplateView, DetailView, ListView 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.db.models import Q, Sum 
from .forms import CustomUserCreationForm, CampanaForm 
from .models import Campana, Categoria, Donacion 
from .forms import CustomUserCreationForm, CampanaForm, DonacionForm, CustomPasswordChangeForm
from django.http import JsonResponse 
from django.views.decorators.http import require_POST
from django.contrib.auth.views import PasswordChangeView

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


# Vista para el Listado de Campañas con Búsqueda/Filtro (Requisito 12)
class CampanaListView(ListView):
    model = Campana
    template_name = 'core/campana_list.html'
    context_object_name = 'campanas'
    paginate_by = 9

    def get_queryset(self):
        from django.db.models import Count
        
        # Filtra solo las campañas activas y añade el conteo de donaciones
        # CONEXIÓN DOBLE: Campana → Donacion (COUNT)
        queryset = super().get_queryset().filter(estado='ACT').annotate(
            num_donaciones=Count('donaciones')
        )
        
        # Búsqueda por palabra clave (query)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) | Q(descripcion__icontains=query)
            ).distinct()

        # Filtrado por Categoría
        categoria_id = self.request.GET.get('cat')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)

        # Ordenamiento (nuevo parámetro)
        orden = self.request.GET.get('orden', 'recientes')
        if orden == 'populares':
            # Ordena por número de donaciones (descendente)
            queryset = queryset.order_by('-num_donaciones', '-fecha_creacion')
        elif orden == 'recaudado':
            # Ordena por monto recaudado (descendente)
            queryset = queryset.order_by('-recaudado', '-fecha_creacion')
        else:  # recientes (por defecto)
            queryset = queryset.order_by('-fecha_creacion')

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasa todas las categorías para el menú de filtro
        context['categorias'] = Categoria.objects.all() 
        context['current_cat'] = self.request.GET.get('cat')
        context['current_query'] = self.request.GET.get('q')
        context['current_orden'] = self.request.GET.get('orden', 'recientes')
        return context


# Vista para el Detalle de Campaña (Requisito 2)
class CampanaDetailView(DetailView):
    model = Campana
    template_name = 'core/campana_detail.html'
    context_object_name = 'campana'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añade el formulario de donación y donaciones recientes
        context['form_donacion'] = DonacionForm() 
        context['donaciones'] = self.object.donaciones.all().order_by('-fecha_donacion')[:5]
        return context


# # Función para procesar la donación (POST)
# @login_required
# def donar_submit_view(request, pk):
#     campana = get_object_or_404(Campana, pk=pk)
    
#     if request.method == 'POST':
#         form = DonacionForm(request.POST)
#         if form.is_valid():
#             donacion = form.save(commit=False)
#             donacion.campana = campana
#             donacion.donante = request.user
#             donacion.save()

#             # Lógica de actualización de recaudación
#             if donacion.tipo == 'MON' and donacion.monto:
#                 # Usamos una operación segura de suma
#                 campana.recaudado = (campana.recaudado or 0) + donacion.monto
#                 campana.save()
            
#             messages.success(request, f'¡Gracias {request.user.username}! Tu donación de {donacion.get_tipo_display()} ha sido registrada con éxito.')
#         else:
#             # Si hay un error, lo mostramos y redirigimos de vuelta al detalle
#             messages.error(request, f'Error en la donación: Revise si ingresó monto O artículo. {form.errors}')
            
#     return redirect('campana_detalle', pk=campana.pk)

@login_required
@require_POST # Asegura que solo acepte peticiones POST
def donar_submit_view(request, pk):
    campana = get_object_or_404(Campana, pk=pk)
    
    # Asume que esta vista será llamada por AJAX, devolviendo JSON.
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = DonacionForm(request.POST)
        
        if form.is_valid():
            try:
                donacion = form.save(commit=False)
                donacion.campana = campana
                donacion.donante = request.user
                donacion.save()

                # Lógica de actualización de recaudación
                if donacion.tipo == 'MON' and donacion.monto:
                    campana.recaudado = (campana.recaudado or 0) + donacion.monto
                    campana.save(update_fields=['recaudado', 'recaudado'])
                
                # Devuelve JSON de éxito
                return JsonResponse({
                    'success': True,
                    'message': f'¡Gracias {request.user.username}! Tu donación ha sido registrada.',
                    'new_recaudado': float(campana.recaudado),
                    'new_porcentaje': campana.porcentaje_completado,
                })
            except Exception as e:
                 return JsonResponse({'success': False, 'message': 'Error al procesar la donación.'}, status=500)
        else:
            # Devuelve JSON con errores del formulario
            errors = dict(form.errors)
            return JsonResponse({'success': False, 'errors': errors, 'message': 'Datos del formulario inválidos.'}, status=400)
            
    # Si no es AJAX, redirige como fallback
    messages.error(request, 'Error en el método de envío. Intente de nuevo.')
    return redirect('campana_detalle', pk=campana.pk)

class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Campañas que el usuario ha organizado
        mis_campanas = user.campana_set.all().order_by('-fecha_creacion')
        context['mis_campanas'] = mis_campanas
        
        # Donaciones que el usuario ha realizado
        mis_donaciones = user.donaciones_realizadas.all().order_by('-fecha_donacion')
        context['mis_donaciones'] = mis_donaciones

        # Métricas rápidas para mostrar en el perfil/dashboard
        context['total_campanas'] = mis_campanas.count()
        agg = mis_donaciones.filter(tipo='MON').aggregate(total=Sum('monto'))
        context['total_donado'] = agg['total'] or 0
        context['ultima_donacion'] = mis_donaciones.first()
        
        return context
    
# Nueva Vista para Editar Campaña
class CampanaUpdateView(LoginRequiredMixin, UpdateView):
    model = Campana
    form_class = CampanaForm
    template_name = 'core/campana_form.html' # Reutilizamos la misma plantilla
    success_url = reverse_lazy('dashboard') 

    # Implementación de Autorización (Req 4)
    def dispatch(self, request, *args, **kwargs):
        # Primero llama al dispatch de LoginRequiredMixin para asegurar que el usuario esté logueado
        response = super().dispatch(request, *args, **kwargs)
        
        # Obtener la campaña a editar
        campana = self.get_object()
        
        # Comprueba si el usuario logueado NO es el organizador
        if campana.organizador != self.request.user:
            # Lanza una excepción o redirige a un mensaje de error
            messages.error(request, "No tienes permiso para editar esta campaña.")
            raise PermissionDenied
            
        return response

    # Opcional: Cambia el título de la plantilla para que sepa que está editando
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_title'] = "Editar Campaña"
        return context


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Vista personalizada para cambiar contraseña sin crispy."""
    template_name = 'registration/password_change_form.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('perfil')

    def form_valid(self, form):
        messages.success(self.request, 'Tu contraseña fue actualizada correctamente.')
        return super().form_valid(form)