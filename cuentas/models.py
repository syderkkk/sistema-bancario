from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

class CuentaBancaria(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cuentas')
    numero_cuenta = models.CharField(max_length=20, unique=True)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    clave_secreta = models.CharField(max_length=128, blank=True, null=True)  # <-- Campo agregado

    def __str__(self): return f"Cuenta {self.numero_cuenta} - Saldo: {self.saldo}"
    
    def set_clave_secreta(self, clave):
        #self.clave_secreta = make_password(clave)
        self.clave_secreta = clave
        
    def verificar_clave(self, clave):
        #return check_password(clave, self.clave_secreta)
        return self.clave_secreta == clave

    def clean(self):
        if self.saldo < 0: raise ValueError("El saldo no puede ser negativo.")

class TarjetaBancaria(models.Model):
    cuenta = models.ForeignKey(CuentaBancaria, on_delete=models.CASCADE, related_name='tarjeta')
    numero_tarjeta = models.CharField(max_length=16, unique=True)
    fecha_vencimiento = models.DateField()
    cvv = models.CharField(max_length=3)
    creada = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): return f"Tarjeta {self.numero_tarjeta} - Cuenta: {self.cuenta.numero_cuenta}"
