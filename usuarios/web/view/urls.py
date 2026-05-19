from django.urls import path
from .listar import UsuariosListView

urlpatterns = [
    path('', UsuariosListView.as_view(), name='usuarios_listar'),
]