from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from utils.pila import Pila



# Create your views here.
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
    return render(request, 'auditoria/historial_sesiones.html', {
        'sesiones': sesiones,
        'usuarios': usuarios,
        'usuario_seleccionado': usuario
    })