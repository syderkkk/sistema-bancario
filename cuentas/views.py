from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from cuentas.models import CuentaBancaria
from cuentas.services import crear_tarjeta_para_cuenta

from .forms import TransferenciaForm
from django.contrib import messages

from cuentas.models import TarjetaBancaria
from transacciones.models import Transaccion




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from cuentas.models import CuentaBancaria
from cuentas.services import crear_tarjeta_para_cuenta
from .forms import TransferenciaForm
from django.contrib import messages
from transacciones.models import Transaccion
from django.db import models


@login_required
def detalle_cuenta(request, cuenta_id):
    cuenta = get_object_or_404(CuentaBancaria, id=cuenta_id, usuario=request.user)
    transferencia_form = TransferenciaForm()
    # Obtener historial de transacciones (ingresos y salidas)
    transacciones = Transaccion.objects.filter(
        models.Q(cuenta_origen=cuenta) | models.Q(cuenta_destino=cuenta)
    ).order_by('-fecha')
    if request.method == "POST":
        if "generar_tarjeta" in request.POST:
            if not cuenta.tarjeta.exists():
                crear_tarjeta_para_cuenta(cuenta)
            tarjeta = cuenta.tarjeta.first()
            if tarjeta:
                return redirect('detalle_tarjeta', tarjeta_id=tarjeta.id)
    return render(request, 'cuentas/detalle_cuenta.html', {
        'cuenta': cuenta,
        'transferencia_form': transferencia_form,
        'transacciones': transacciones
    })


@login_required
def transferir(request, cuenta_id):
    cuenta = get_object_or_404(CuentaBancaria, id=cuenta_id, usuario=request.user)
    transferencia_form = TransferenciaForm()
    if request.method == "POST":
        transferencia_form = TransferenciaForm(request.POST)
        if transferencia_form.is_valid():
            numero_destino = transferencia_form.cleaned_data["numero_cuenta_destino"]
            monto = transferencia_form.cleaned_data["monto"]
            descripcion = transferencia_form.cleaned_data["descripcion"]
            try:
                from cuentas.services import transferir_fondos
                cuenta_destino = CuentaBancaria.objects.get(numero_cuenta=numero_destino)
                if cuenta_destino.id == cuenta.id:
                    messages.error(request, "No puedes transferir a la misma cuenta.")
                else:
                    transaccion = transferir_fondos(cuenta, cuenta_destino, monto, descripcion)
                    titular_destino = f"{cuenta_destino.usuario.first_name} {cuenta_destino.usuario.last_name}"
                    return render(request, 'cuentas/transferencia_exitosa.html', {
                        'cuenta_origen': cuenta,
                        'cuenta_destino': cuenta_destino,
                        'monto': monto,
                        'descripcion': descripcion,
                        'titular_destino': titular_destino,
                        'transaccion': transaccion
                    })
            except CuentaBancaria.DoesNotExist:
                messages.error(request, "La cuenta destino no existe.")
            except ValueError as e:
                messages.error(request, str(e))
    return render(request, 'cuentas/transferir.html', {
        'cuenta': cuenta,
        'transferencia_form': transferencia_form
    })


from .forms import CajeroForm
from cuentas.services import depositar_fondos, retirar_fondos

def cajero(request):
    deposito_form = CajeroForm(prefix="deposito")
    retiro_form = CajeroForm(prefix="retiro")
    resultado = None
    error = None

    if request.method == "POST":
        if "depositar" in request.POST:
            deposito_form = CajeroForm(request.POST, prefix="deposito")
            if deposito_form.is_valid():
                numero_cuenta = deposito_form.cleaned_data["numero_cuenta"]
                monto = deposito_form.cleaned_data["monto"]
                try:
                    cuenta = CuentaBancaria.objects.get(numero_cuenta=numero_cuenta)
                    depositar_fondos(cuenta, monto, descripcion="Depósito en cajero físico simulado")
                    resultado = {
                        "tipo": "depósito",
                        "cuenta": cuenta,
                        "monto": monto
                    }
                except CuentaBancaria.DoesNotExist:
                    error = "La cuenta no existe."
        elif "retirar" in request.POST:
            retiro_form = CajeroForm(request.POST, prefix="retiro")
            if retiro_form.is_valid():
                numero_cuenta = retiro_form.cleaned_data["numero_cuenta"]
                monto = retiro_form.cleaned_data["monto"]
                try:
                    cuenta = CuentaBancaria.objects.get(numero_cuenta=numero_cuenta)
                    retirar_fondos(cuenta, monto, descripcion="Retiro en cajero físico simulado")
                    resultado = {
                        "tipo": "retiro",
                        "cuenta": cuenta,
                        "monto": monto
                    }
                except CuentaBancaria.DoesNotExist:
                    error = "La cuenta no existe."
                except ValueError as e:
                    error = str(e)
    return render(request, "cuentas/cajero.html", {
        "deposito_form": deposito_form,
        "retiro_form": retiro_form,
        "resultado": resultado,
        "error": error
    })

@login_required
def detalle_tarjeta(request, tarjeta_id):
    tarjeta = get_object_or_404(TarjetaBancaria, id=tarjeta_id)
    if tarjeta.cuenta.usuario != request.user:
        return redirect('home')
    return render(request, 'cuentas/detalle_tarjeta.html', {'tarjeta': tarjeta})

@login_required
def eliminar_tarjeta(request, tarjeta_id):
    tarjeta = get_object_or_404(TarjetaBancaria, id=tarjeta_id)
    # Verifica que la tarjeta pertenezca a una cuenta del usuario autenticado
    if tarjeta.cuenta.usuario != request.user:
        return redirect('home')
    cuenta_id = tarjeta.cuenta.id
    if request.method == "POST":
        tarjeta.delete()
        return redirect('detalle_cuenta', cuenta_id=cuenta_id)
    return redirect('detalle_tarjeta', tarjeta_id=tarjeta_id)

@login_required
def eliminar_cuenta(request, cuenta_id):
    cuenta = get_object_or_404(CuentaBancaria, id=cuenta_id, usuario=request.user)
    if request.method == "POST":
        cuenta.delete()
        return redirect('home')
    return redirect('detalle_cuenta', cuenta_id=cuenta_id)