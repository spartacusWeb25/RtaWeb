from django.urls import path
from .listar import CargosListView

urlpatterns = [
    path('', CargosListView.as_view(), name='cargos_listar'),
]