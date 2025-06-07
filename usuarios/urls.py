from django.urls import path, include
from usuarios.views import (
    RegistroUsuarioView,
    CustomLoginView,
    home,
    logout_view,
    editar_perfil,
    gestionar_solicitudes_prestamo,
    cambiar_estado_solicitud,
    solicitar_prestamo,
    historial_sesiones,
)

urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
    path('prestamos/gestionar/', gestionar_solicitudes_prestamo, name='gestionar_solicitudes_prestamo'),
    path('prestamos/solicitud/<int:solicitud_id>/cambiar_estado/', cambiar_estado_solicitud, name='cambiar_estado_solicitud'),
    path('prestamos/solicitar/<int:cuenta_id>/', solicitar_prestamo, name='solicitar_prestamo'),
    path('historial-sesiones/', historial_sesiones, name='historial_sesiones'),
]