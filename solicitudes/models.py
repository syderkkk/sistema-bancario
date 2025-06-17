from django.db import models
from django.contrib.auth.models import User
from cuentas.models import CuentaBancaria

# Create your models here.
class SolicitudPrestamo(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_prestamo')
    cuenta = models.ForeignKey(CuentaBancaria, on_delete=models.CASCADE, related_name='solicitudes_prestamo')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    plazo_meses = models.PositiveIntegerField()
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    motivo = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self): return f"{self.usuario.username} - S/.{self.monto} - {self.estado}"