from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.http import require_POST

from .forms import RegistroUsuarioForm, EditarPerfilForm
from auditoria.models import HistorialInicioSesion
from cuentas.services import crear_cuenta
from utils.lista_circular import ListaCircular
from django.contrib import messages

# Vista para el registro de nuevos usuarios
class RegistroUsuarioView(CreateView):
    model = User
    form_class = RegistroUsuarioForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        usuario = self.request.user
        ip = self.request.META.get('REMOTE_ADDR')
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        HistorialInicioSesion.objects.create(
            usuario=usuario,
            ip=ip,
            user_agent=user_agent
        )
        return response

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    imagenes = [
        'usuarios/carrusel/promo1.jpg',
        'usuarios/carrusel/promo2.jpg'
    ]
    
    lista = ListaCircular()
    for img in imagenes:
        lista.agregar(img)

    try:
        pos = int(request.GET.get('pos', 0))
    except ValueError:
        pos = 0

    longitud = lista.longitud()
    if longitud == 0:
        imagen_actual = None
    else:
        pos = pos % longitud  # Circular
        nodo = lista.buscar(pos)
        imagen_actual = nodo.imagen

    return render(request, 'usuarios/landing.html', {
        'imagen_actual': imagen_actual,
        'pos': pos,
        'longitud': longitud
    })

# Vista para la página de inicio después de iniciar sesión
@login_required
def home(request):
    cuentas = request.user.cuentas.all()
    if request.method == 'POST' and 'crear_cuenta' in request.POST:
        try:
            crear_cuenta(request.user, None)
        except ValueError as e:
            messages.error(request, str(e))
        return redirect('home')
    return render(request, 'usuarios/home.html', {'cuentas': cuentas})

# Vista para cerrar sesión
@require_POST
def logout_view(request):
    logout(request)
    return redirect('landing_page')

@login_required
def editar_perfil(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('editar_perfil')
    else:
        form = EditarPerfilForm(instance=profile, user=request.user)
    return render(request, 'usuarios/editar_perfil.html', {'form': form})