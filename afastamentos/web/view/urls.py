from django.urls import path
from .listar import AfastamentosListView

urlpatterns = [
    path('', AfastamentosListView.as_view(), name='afastamentos_listar'),
]