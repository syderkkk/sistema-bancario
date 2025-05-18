from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegistroUsuarioForm
from django.contrib.auth.models import User

class RegistroUsuarioView(CreateView):
    """
    Vista para el registro de nuevos usuarios.
    """
    model = User
    form_class = RegistroUsuarioForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('login')