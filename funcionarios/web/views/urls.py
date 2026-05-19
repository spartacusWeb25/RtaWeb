from django.urls import path
from .listar import FuncionarioListView

urlpatterns = [
    path('', FuncionarioListView.as_view(), name='funcionario_listar'),
]