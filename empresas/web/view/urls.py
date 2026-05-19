from django.urls import path
from .listar import EmpresasListView

urlpatterns = [
    path('', EmpresasListView.as_view(), name='empresas_listar'),
]