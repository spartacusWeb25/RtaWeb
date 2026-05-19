from django.urls import path
from .listar import DadosRescisaoListView

urlpatterns = [
    path('', DadosRescisaoListView.as_view(), name='dadosrescisao_listar'),
]