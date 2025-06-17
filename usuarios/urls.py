from django.urls import path
from usuarios.views import (
    RegistroUsuarioView,
    CustomLoginView,
    home,
    logout_view,
    editar_perfil,
)

urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
]