from django.urls import path
from usuarios.web.views.listar import UsuariosListView

urlpatterns = [
    path('', UsuariosListView.as_view(), name='usuarios_listar'),
]