from django.db import models
from cuentas.models import CuentaBancaria

class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('DEPOSITO', 'Deposito'),
        ('RETIRO', 'Retiro'),
        ('TRANSFERENCIA', 'Transferencia'),
    ]
    cuenta_origen = models.ForeignKey(CuentaBancaria, on_delete=models.CASCADE, related_name='transacciones_origen', null=True, blank=True)
    cuenta_destino = models.ForeignKey(CuentaBancaria, on_delete=models.CASCADE, related_name='transacciones_destino', null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.monto} - {self.fecha}"