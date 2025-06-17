from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HistorialInicioSesion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historial_sesiones')
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self): return f"{self.usuario.username} - {self.fecha}"