from django.db import models
from django.conf import settings

class CuentaBancaria(models.Model):
    """
    Modelo para representar una cuenta bancaria.
    """
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cuentas')
    numero_cuenta = models.CharField(max_length=20, unique=True)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cuenta {self.numero_cuenta} - Saldo: {self.saldo}"
    
    def clean(self):
        """
        Método para validar el saldo de la cuenta.
        """
        if self.saldo < 0:
            raise ValueError("El saldo no puede ser negativo.")