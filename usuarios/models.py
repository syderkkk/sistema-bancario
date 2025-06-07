from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cuentas.models import CuentaBancaria

# Modelo para representar el perfil de un usuario
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    numero_cuenta = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self): return f"Perfil de {self.user.username}"

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

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

class HistorialInicioSesion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historial_sesiones')
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self): return f"{self.usuario.username} - {self.fecha}"