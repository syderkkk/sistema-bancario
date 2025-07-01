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
            
            # Validar saldo suficiente antes de transferir
            if cuenta.saldo < monto:
                messages.error(request, "Saldo insuficiente para realizar la transferencia.")
                return render(request, "cuentas/transferir.html", {
                    "cuenta": cuenta,
                    "transferencia_form": form
                })
            
            try:
                cuenta_destino = CuentaBancaria.objects.get(numero_cuenta=numero_cuenta_destino)
                
                # Validar que no sea la misma cuenta
                if cuenta_destino.id == cuenta.id:
                    messages.error(request, "No puedes transferir a la misma cuenta.")
                    return render(request, "cuentas/transferir.html", {
                        "cuenta": cuenta,
                        "transferencia_form": form
                    })
                
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
                
                # Validar que el monto sea positivo
                if monto <= 0:
                    error = "El monto debe ser mayor a 0."
                else:
                    try:
                        cuenta = CuentaBancaria.objects.get(numero_cuenta=numero_cuenta)
                        depositar_fondos(cuenta, monto, descripcion="Depósito en cajero físico simulado")
                        
                        # Refrescar la cuenta para obtener el saldo actualizado
                        cuenta.refresh_from_db()
                        
                        resultado = {
                            "tipo": "depósito",
                            "cuenta": cuenta,
                            "monto": monto
                        }
                        
                        # Limpiar el formulario después de éxito
                        deposito_form = CajeroForm(prefix="deposito")
                        
                    except CuentaBancaria.DoesNotExist:
                        error = "La cuenta no existe."
                    except Exception as e:
                        error = f"Error al procesar el depósito: {str(e)}"
                        
        elif "retirar" in request.POST:
            retiro_form = CajeroForm(request.POST, prefix="retiro")
            clave = request.POST.get("clave")
            
            if retiro_form.is_valid():
                numero_cuenta = retiro_form.cleaned_data["numero_cuenta"]
                monto = retiro_form.cleaned_data["monto"]
                
                # Validar que el monto sea positivo
                if monto <= 0:
                    error = "El monto debe ser mayor a 0."
                elif not clave:
                    error = "La clave secreta es requerida."
                elif len(clave) < 4:
                    error = "La clave debe tener al menos 4 caracteres."
                else:
                    try:
                        cuenta = CuentaBancaria.objects.get(numero_cuenta=numero_cuenta)
                        
                        # Verificar clave secreta
                        if not cuenta.clave_secreta:
                            error = "Esta cuenta no tiene una clave secreta configurada."
                        elif not cuenta.verificar_clave(clave):
                            error = "Clave secreta incorrecta."
                        elif cuenta.saldo < monto:
                            error = "Saldo insuficiente."
                        else:
                            retirar_fondos(cuenta, monto, descripcion="Retiro en cajero físico simulado")
                            
                            # Refrescar la cuenta para obtener el saldo actualizado
                            cuenta.refresh_from_db()
                            
                            resultado = {
                                "tipo": "retiro",
                                "cuenta": cuenta,
                                "monto": monto
                            }
                            
                            # Limpiar el formulario después de éxito
                            retiro_form = CajeroForm(prefix="retiro")
                            
                    except CuentaBancaria.DoesNotExist:
                        error = "La cuenta no existe."
                    except ValueError as e:
                        error = str(e)
                    except Exception as e:
                        error = f"Error al procesar el retiro: {str(e)}"
            else:
                # Si el formulario no es válido, mostrar errores
                if retiro_form.errors:
                    error = "Por favor corrige los errores en el formulario."
                    
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