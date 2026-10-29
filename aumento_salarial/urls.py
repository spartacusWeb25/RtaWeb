from django.urls import path

from aumento_salarial.web.views import atualizar, criar, deletar, listar


app_name = "aumento_salarial"

urlpatterns = [
    path("", listar.AumentoSalarialListView.as_view(), name="listar"),
    path("criar/", criar.AumentoSalarialCreateView.as_view(), name="criar"),
    path("<int:aume_codi>/editar/", atualizar.AumentoSalarialUpdateView.as_view(), name="editar"),
    path("<int:aume_codi>/excluir/", deletar.AumentoSalarialDeleteView.as_view(), name="excluir"),
]
