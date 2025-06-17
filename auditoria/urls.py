from django.urls import path
from .views import historial_sesiones

urlpatterns = [
    path('historial-sesiones/', historial_sesiones, name='historial_sesiones'),
]