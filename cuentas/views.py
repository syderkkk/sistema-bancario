from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.db.models import Q

from cuentas.models import CuentaBancaria, TarjetaBancaria
from cuentas.services import crear_tarjeta_para_cuenta, depositar_fondos, retirar_fondos
from transacciones.models import Transaccion
from .forms import TransferenciaForm, CajeroForm, ClaveSecretaForm

from utils.lista_enlazada import HistorialTransacciones
from utils.filtros_transacciones import filtrar_y_ordenar_transacciones
from .services import transferir_fondos, crear_cuenta

@login_required
def detalle_cuenta(request, cuenta_id):
    cuenta = get_object_or_404(CuentaBancaria, id=cuenta_id, usuario=request.user)
    transferencia_form = TransferenciaForm()
    transacciones_qs = Transaccion.objects.filter(
        models.Q(cuenta_origen=cuenta) | models.Q(cuenta_destino=cuenta)
    ).order_by('fecha')

    historial = HistorialTransacciones(L=5)
    
    for t in transacciones_qs:
        historial.agregar(t)
    if request.method == "POST":
        if "generar_tarjeta" in request.POST and not cuenta.tarjeta.exists():
            crear_tarjeta_para_cuenta(cuenta)
        tarjeta = cuenta.tarjeta.first()
        if tarjeta:
            return redirect('detalle_tarjeta', tarjeta_id=tarjeta.id)
    return render(request, 'cuentas/detalle_cuenta.html', {
        'cuenta': cuenta,
        'transferencia_form': transferencia_form,
        'transacciones': historial.iterar_recientes()
    })

@login_required
def transferir(request, cuenta_id):
    cuenta = get_object_or_404(CuentaBancaria, id=cuenta_id, usuario=request.user)
    if request.method == "POST":
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            numero_cuenta_destino = form.cleaned_data["numero_cuenta_destino"]
            monto = form.cleaned_data["monto"]
            descripcion = form.cleaned_data["descripcion"]
            try:
                cuenta_destino = CuentaBancaria.objects.get(numero_cuenta=numero_cuenta_destino)
                transaccion = transferir_fondos(
                    cuenta, cuenta_destino, monto, descripcion
                )
                titular_destino = f"{cuenta_destino.usuario.first_name} {cuenta_destino.usuario.last_name}"
                return render(request, "cuentas/transferencia_exitosa.html", {
                    "cuenta_origen": cuenta,
                    "cuenta_destino": cuenta_destino,
                    "monto": monto,
                    "descripcion": descripcion,
                    "titular_destino": titular_destino,
                    "transaccion": transaccion
                })
            except CuentaBancaria.DoesNotExist:
                messages.error(request, "La cuenta destino no existe.")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = TransferenciaForm()
    return render(request, "cuentas/transferir.html", {
        "cuenta": cuenta,
        "transferencia_form": form
    })


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
            clave = request.POST.get("clave")
            if retiro_form.is_valid():
                numero_cuenta = retiro_form.cleaned_data["numero_cuenta"]
                monto = retiro_form.cleaned_data["monto"]
                try:
                    cuenta = CuentaBancaria.objects.get(numero_cuenta=numero_cuenta)
                    if not cuenta.verificar_clave(clave):
                        error = "Clave secreta incorrecta."
                    else:
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

@login_required
def movimientos_cuenta(request, cuenta_id):
    cuenta = get_object_or_404(CuentaBancaria, id=cuenta_id, usuario=request.user)
    filtros = {
        'tipo': request.GET.get('tipo') or '',
        'fecha_inicio': request.GET.get('fecha_inicio') or '',
        'fecha_fin': request.GET.get('fecha_fin') or '',
        'orden': request.GET.get('orden', 'fecha_desc'),
        'monto_min': request.GET.get('monto_min') or '',
        'monto_max': request.GET.get('monto_max') or '',
        'descripcion': request.GET.get('descripcion') or '',
    }

    transacciones_qs = Transaccion.objects.filter(
        Q(cuenta_origen=cuenta) | Q(cuenta_destino=cuenta)
    )

    transacciones = filtrar_y_ordenar_transacciones(transacciones_qs, filtros)

    return render(request, 'cuentas/movimientos_cuenta.html', {
        'cuenta': cuenta,
        'transacciones': transacciones,
        **filtros,
    })

@login_required
def crear_cuenta_con_clave(request):
    if request.method == "POST":
        form = ClaveSecretaForm(request.POST)
        if form.is_valid():
            cuenta = crear_cuenta(request.user, numero_cuenta=None)
            cuenta.set_clave_secreta(form.cleaned_data['clave'])
            cuenta.save()
            return redirect('home')
    else:
        form = ClaveSecretaForm()
    return render(request, 'cuentas/crear_cuenta_con_clave.html', {'form': form})