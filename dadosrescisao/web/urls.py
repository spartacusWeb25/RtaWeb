from django.urls import path
from dadosrescisao.web.views.listar import DadosRescisaoListView

app_name = 'dadosrescisao'

urlpatterns = [
    path('', DadosRescisaoListView.as_view(), name='dadosrescisao_listar'),
]