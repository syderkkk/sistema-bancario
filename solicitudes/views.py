from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import SolicitudPrestamo
from .forms import SolicitudPrestamoForm
from cuentas.models import CuentaBancaria
from utils.cola import ColaSolicitudes

# Create your views here.
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
            return render(request, 'solicitudes/solicitud_prestamo_enviada.html')
    else:
        form = SolicitudPrestamoForm()
    return render(request, 'solicitudes/solicitar_prestamo.html', {
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
    return render(request, 'solicitudes/gestionar_solicitudes_prestamo.html', {
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