from django.urls import path

from tabelairrf.web.views.criar import TabelairrfCreateView
from tabelairrf.web.views.deletar import TabelairrfDeleteView
from tabelairrf.web.views.editar import TabelairrfUpdateView
from tabelairrf.web.views.listar import TabelairrfListView

app_name = "tabelairrf"

urlpatterns = [
    path("", TabelairrfListView.as_view(), name="listar"),
    path("criar/", TabelairrfCreateView.as_view(), name="irrf_criar"),
    path("editar/<str:irrf_refe>/", TabelairrfUpdateView.as_view(), name="irrf_editar"),
    path("deletar/<str:irrf_refe>/", TabelairrfDeleteView.as_view(), name="irrf_deletar"),
]
