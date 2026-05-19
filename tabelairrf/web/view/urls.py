from django.urls import path
from .listar import TabelairrfListView

urlpatterns = [
    path('', TabelairrfListView.as_view(), name='tabelairrf_listar'),
]