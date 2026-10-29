from django.urls import path

from eventos_agrupados.web.views import atualizar, criar, deletar, listar


app_name = "eventos_agrupados"

urlpatterns = [
    path("", listar.EventosAgrupadosListView.as_view(), name="listar"),
    path("criar/", criar.EventosAgrupadosCreateView.as_view(), name="criar"),
    path("editar/", atualizar.EventosAgrupadosUpdateView.as_view(), name="editar"),
    path("excluir/", deletar.EventosAgrupadosDeleteView.as_view(), name="excluir"),
]
