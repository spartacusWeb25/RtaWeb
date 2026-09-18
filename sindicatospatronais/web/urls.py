from django.urls import path

from sindicatospatronais.web.views.criar import SindicatoPatronalCreateView
from sindicatospatronais.web.views.deletar import SindicatoPatronalDeleteView
from sindicatospatronais.web.views.listar import SindicatosPatronaisListView
from sindicatospatronais.web.views.atualizar import SindicatoPatronalUpdateView

app_name = "sindicatospatronais"

urlpatterns = [
    path("", SindicatosPatronaisListView.as_view(), name="listar"),
    path("novo/", SindicatoPatronalCreateView.as_view(), name="criar"),
    path("<int:empr>/<int:fili>/<int:codi>/editar/", SindicatoPatronalUpdateView.as_view(), name="atualizar"),
    path("<int:empr>/<int:fili>/<int:codi>/excluir/", SindicatoPatronalDeleteView.as_view(), name="deletar"),
]
