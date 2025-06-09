from django.urls import path, include
from . import views

urlpatterns = [
    path('cuenta/<int:cuenta_id>/', views.detalle_cuenta, name='detalle_cuenta'),
    path('cuenta/<int:cuenta_id>/eliminar/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('cuenta/<int:cuenta_id>/transferir/', views.transferir, name='transferir'),
    path('cuenta/<int:cuenta_id>/movimientos/', views.movimientos_cuenta, name='movimientos_cuenta'),
    path('tarjeta/<int:tarjeta_id>/', views.detalle_tarjeta, name='detalle_tarjeta'),
    path('tarjeta/<int:tarjeta_id>/eliminar/', views.eliminar_tarjeta, name='eliminar_tarjeta'),
    path('cajero/', views.cajero, name='cajero'),

    path('cuenta/nueva/', views.crear_cuenta_con_clave, name='crear_cuenta_con_clave'),
]