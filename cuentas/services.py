from django.db import transaction
from transacciones.models import Transaccion
from .models import CuentaBancaria, TarjetaBancaria
from datetime import date, timedelta
import random

# Función para generar un número de cuenta único de 5 digitos
def generar_numero_cuenta():
    while True:
        numero = str(random.randint(10**4, 10**5 - 1))
        if not CuentaBancaria.objects.filter(numero_cuenta=numero).exists(): return numero

# Función para crear una nueva cuenta bancaria
def crear_cuenta(usuario, numero_cuenta, saldo_inicial=0.00):
    if usuario.cuentas.count() >= 5:
        raise ValueError("No puedes tener más de 5 cuentas bancarias.")
    numero_cuenta = generar_numero_cuenta()
    with transaction.atomic():
        cuenta = CuentaBancaria.objects.create(
            usuario=usuario,
            numero_cuenta=numero_cuenta,
            saldo=saldo_inicial
        )
        return cuenta

# Función para depositar fondos en una cuenta bancaria
def depositar_fondos(cuenta, monto, descripcion=""):
    with transaction.atomic():
        cuenta.saldo += monto
        cuenta.save()
    Transaccion.objects.create(
        cuenta_origen=cuenta,
        tipo='DEPOSITO',
        monto=monto,
        descripcion=descripcion
    )

# Función para retirar fondos de una cuenta bancaria
def retirar_fondos(cuenta, monto, descripcion=""):
    with transaction.atomic():
        if cuenta.saldo < monto: raise ValueError("Saldo insuficiente")
        cuenta.saldo -= monto
        cuenta.save()
    Transaccion.objects.create(
        cuenta_origen=cuenta,
        tipo='RETIRO',
        monto=monto,
        descripcion=descripcion
    )

def transferir_fondos(cuenta_origen, cuenta_destino, monto, descripcion=""):
    with transaction.atomic():
        cuenta_origen.saldo -= monto
        cuenta_destino.saldo += monto
        cuenta_origen.save()
        cuenta_destino.save()
    transaccion = Transaccion.objects.create(
        cuenta_origen=cuenta_origen,
        cuenta_destino=cuenta_destino,
        tipo='TRANSFERENCIA',
        monto=monto,
        descripcion=descripcion
    )
    return transaccion

# Función para generar un número de tarjeta único de 16 digitos
def generar_numero_tarjeta():
    while True:
        numero = str(random.randint(10**15, 10**16 - 1))
        if not TarjetaBancaria.objects.filter(numero_tarjeta=numero).exists():
            return numero
        
# Función para generar un código CVV de 3 digitos
def generar_cvv(): return str(random.randint(100, 999))

def crear_tarjeta_para_cuenta(cuenta):
    numero_tarjeta = generar_numero_tarjeta()
    cvv = generar_cvv()
    fecha_vencimiento = date.today() + timedelta(days=365*4)  # 4 años
    tarjeta = TarjetaBancaria.objects.create(
        cuenta=cuenta,
        numero_tarjeta=numero_tarjeta,
        fecha_vencimiento=fecha_vencimiento,
        cvv=cvv
    )
    return tarjeta