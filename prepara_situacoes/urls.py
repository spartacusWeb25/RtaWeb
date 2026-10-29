from django.urls import path

from prepara_situacoes.web.views import atualizar, criar, deletar, listar


app_name = "prepara_situacoes"

urlpatterns = [
    path("", listar.PreparaSituacoesListView.as_view(), name="listar"),
    path("criar/", criar.PreparaSituacoesCreateView.as_view(), name="criar"),
    path("<int:prep_codi>/editar/", atualizar.PreparaSituacoesUpdateView.as_view(), name="editar"),
    path("<int:prep_codi>/excluir/", deletar.PreparaSituacoesDeleteView.as_view(), name="excluir"),
]
