from django.urls import path
from .listar import TabelainssListView

urlpatterns = [
    path('', TabelainssListView.as_view(), name='tabelainss_listar'),
]