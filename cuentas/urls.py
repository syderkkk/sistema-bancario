from django.urls import path
from . import views

urlpatterns = [
    path('cuenta/<int:cuenta_id>/', views.detalle_cuenta, name='detalle_cuenta'),
    path('tarjeta/<int:tarjeta_id>/', views.detalle_tarjeta, name='detalle_tarjeta'),
]