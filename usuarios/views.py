from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegistroUsuarioForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class RegistroUsuarioView(CreateView):
    """
    Vista para el registro de nuevos usuarios.
    """
    model = User
    form_class = RegistroUsuarioForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('login')


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
    return render(request, 'usuarios/landing.html')

@login_required
def home(request):
    """
    Vista para la página de inicio después de iniciar sesión.
    """
    return render(request, 'usuarios/home.html')


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST
def logout_view(request):
    """
    Vista para cerrar sesión.
    """
    logout(request)
    return redirect('landing_page')