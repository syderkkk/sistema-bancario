from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegistroUsuarioForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

class RegistroUsuarioView(CreateView):
    """
    Vista para el registro de nuevos usuarios.
    """
    model = User
    form_class = RegistroUsuarioForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    """
    Vista personalizada para el inicio de sesión.
    """
    template_name = 'usuarios/login.html'
    success_url = reverse_lazy('usuarios/home.html')
    #redirect_authenticated_user = True

def landing_page(request):
    """
    Vista para la página de inicio.
    """
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'usuarios/landing.html')

from cuentas.services import crear_cuenta
@login_required
def home(request):
    """
    Vista para la página de inicio después de iniciar sesión.
    """
    cuentas = request.user.cuentas.all()
    if request.method == 'POST' and 'crear_cuenta' in request.POST:
        crear_cuenta(request.user, None)
        return redirect('home')
    return render(request, 'usuarios/home.html', {'cuentas': cuentas})

@require_POST
def logout_view(request):
    """
    Vista para cerrar sesión.
    """
    logout(request)
    return redirect('landing_page')

from .forms import EditarPerfilForm
@login_required
def editar_perfil(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditarPerfilForm(instance=profile, user=request.user)
    return render(request, 'usuarios/editar_perfil.html', {'form': form})