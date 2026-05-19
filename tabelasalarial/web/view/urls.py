from django.urls import path
from .listar import TabelasalarialListView

urlpatterns = [
    path('', TabelasalarialListView.as_view(), name='tabelasalarial_listar'),
]