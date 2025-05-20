from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from cuentas.models import CuentaBancaria
from cuentas.services import crear_tarjeta_para_cuenta

@login_required
def detalle_cuenta(request, cuenta_id):
    cuenta = get_object_or_404(CuentaBancaria, id=cuenta_id, usuario=request.user)
    if request.method == "POST" and "generar_tarjeta" in request.POST:
        if not cuenta.tarjeta.exists():
            crear_tarjeta_para_cuenta(cuenta)
        tarjeta = cuenta.tarjeta.first()
        if tarjeta:
            return redirect('detalle_tarjeta', tarjeta_id=tarjeta.id)
    return render(request, 'cuentas/detalle_cuenta.html', {'cuenta': cuenta})


from cuentas.models import TarjetaBancaria

@login_required
def detalle_tarjeta(request, tarjeta_id):
    tarjeta = get_object_or_404(TarjetaBancaria, id=tarjeta_id, cuenta__usuario=request.user)
    return render(request, 'cuentas/detalle_tarjeta.html', {'tarjeta': tarjeta})