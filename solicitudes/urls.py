from django.urls import path
from . import views

urlpatterns = [
    path('solicitar/<int:cuenta_id>/', views.solicitar_prestamo, name='solicitar_prestamo'),
    path('gestionar/', views.gestionar_solicitudes_prestamo, name='gestionar_solicitudes_prestamo'),
    path('cambiar_estado/<int:solicitud_id>/', views.cambiar_estado_solicitud, name='cambiar_estado_solicitud'),
]