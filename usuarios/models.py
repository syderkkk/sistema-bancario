from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    if created: Profile.objects.create(user=instance)