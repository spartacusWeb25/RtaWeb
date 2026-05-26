from django.urls import path
from dadosrescisao.web.views.listar import DadosRescisaoListView

urlpatterns = [
    path('', DadosRescisaoListView.as_view(), name='dadosrescisao_listar'),
]