from django.urls import path

from folhamensal.web.views.atualizar import FolhaMensalUpdateView
from folhamensal.web.views.criar import FolhaMensalCreateView
from folhamensal.web.views.deletar import FolhaMensalDeleteView
from folhamensal.web.views.list import FolhaMensalListView
from folhamensal.web.views.listar import FolhaMensalListarView

app_name = "folha"

urlpatterns = [
    path("folha-mensal/", FolhaMensalListView.as_view(), name="folha_mensal_list"),
    path("folha-mensal/list/", FolhaMensalListarView.as_view(), name="folha_mensal_listar"),
    path("folha-mensal/novo/", FolhaMensalCreateView.as_view(), name="folha_mensal_criar"),
    path("folha-mensal/<int:fome_func>/<str:fome_refe>/<int:fome_even>/editar/", FolhaMensalUpdateView.as_view(), name="folha_mensal_atualizar"),
    path("folha-mensal/<int:fome_func>/<str:fome_refe>/<int:fome_even>/excluir/", FolhaMensalDeleteView.as_view(), name="folha_mensal_deletar"),
]
