from django.urls import path

from terceiros.web.views.criar import TerceiroCreateView
from terceiros.web.views.deletar import TerceiroDeleteView
from terceiros.web.views.listar import TerceirosListView
from terceiros.web.views.atualizar import TerceiroUpdateView

app_name = "terceiros"

urlpatterns = [
    path("", TerceirosListView.as_view(), name="listar"),
    path("novo/", TerceiroCreateView.as_view(), name="criar"),
    path("<int:empr>/<int:fili>/<int:codi>/editar/", TerceiroUpdateView.as_view(), name="atualizar"),
    path("<int:empr>/<int:fili>/<int:codi>/excluir/", TerceiroDeleteView.as_view(), name="deletar"),
]
