from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

from .forms import RegistroUsuarioForm, EditarPerfilForm, SolicitudPrestamoForm
from .models import HistorialInicioSesion, SolicitudPrestamo
from cuentas.models import CuentaBancaria
from cuentas.services import crear_cuenta
from utils.lista_circular import ListaCircular
from utils.cola import ColaSolicitudes
from utils.pila import Pila
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
            return redirect('home')
    else:
        form = EditarPerfilForm(instance=profile, user=request.user)
    return render(request, 'usuarios/editar_perfil.html', {'form': form})

@login_required
def solicitar_prestamo(request, cuenta_id):
    tasa_interes = 10.0  # Puedes parametrizar esto
    cuenta = CuentaBancaria.objects.get(id=cuenta_id, usuario=request.user)
    if request.method == 'POST':
        form = SolicitudPrestamoForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario = request.user
            solicitud.cuenta = cuenta
            solicitud.tasa_interes = tasa_interes
            solicitud.save()
            return render(request, 'usuarios/solicitud_prestamo_enviada.html')
    else:
        form = SolicitudPrestamoForm()
    return render(request, 'usuarios/solicitar_prestamo.html', {
        'form': form,
        'tasa_interes': tasa_interes,
        'cuenta': cuenta,
    })

@login_required
def gestionar_solicitudes_prestamo(request):
    if not request.user.is_superuser:
        return redirect('home')
    pendientes_qs = SolicitudPrestamo.objects.filter(estado='pendiente').order_by('fecha_solicitud')
    cola = ColaSolicitudes()
    for solicitud in pendientes_qs:
        cola.encolar(solicitud)
    primera_pendiente = cola.ver_frente()
    solicitudes_en_cola = []
    actual = cola.frente
    while actual:
        solicitudes_en_cola.append(actual.solicitud)
        actual = actual.siguiente
    gestionadas = SolicitudPrestamo.objects.exclude(estado='pendiente').order_by('-fecha_solicitud')
    return render(request, 'usuarios/gestionar_solicitudes_prestamo.html', {
        'pendientes': solicitudes_en_cola,
        'gestionadas': gestionadas,
        'primera_pendiente': primera_pendiente,
    })

@login_required
def cambiar_estado_solicitud(request, solicitud_id):
    if not request.user.is_superuser:
        return redirect('home')
    solicitud = get_object_or_404(SolicitudPrestamo, id=solicitud_id)
    accion = request.POST.get('accion')
    if solicitud.estado == 'pendiente':
        if accion == 'aceptar':
            solicitud.estado = 'aceptada'
            cuenta = solicitud.cuenta
            cuenta.saldo += solicitud.monto
            cuenta.save()
        elif accion == 'rechazar':
            solicitud.estado = 'rechazada'
        solicitud.save()
    return redirect('gestionar_solicitudes_prestamo')

@login_required
def historial_sesiones(request):
    if not request.user.is_superuser: return HttpResponseForbidden("No tienes permiso para ver este historial!")
    usuarios = User.objects.all().order_by('username')
    usuario_id = request.GET.get('usuario_id')
    if usuario_id:
        usuario = User.objects.filter(id=usuario_id).first()
    else:
        usuario = None
    sesiones_qs = usuario.historial_sesiones.all()[:10] if usuario else []
    pila = Pila()
    for sesion in sesiones_qs:
        pila.apilar(sesion)
    sesiones = pila.recorrer()
    return render(request, 'usuarios/historial_sesiones.html', {
        'sesiones': sesiones,
        'usuarios': usuarios,
        'usuario_seleccionado': usuario
    })