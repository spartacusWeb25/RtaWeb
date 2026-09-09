from django.urls import path

from contribuintes.web.views.criar import ContribuinteCreateView
from contribuintes.web.views.deletar import ContribuinteDeleteView
from contribuintes.web.views.listar import ContribuintesListView
from contribuintes.web.views.atualizar import ContribuinteUpdateView

app_name = "contribuintes"

urlpatterns = [
    path("", ContribuintesListView.as_view(), name="listar"),
    path("novo/", ContribuinteCreateView.as_view(), name="criar"),
    path("<int:empr>/<int:fili>/<int:codi>/editar/", ContribuinteUpdateView.as_view(), name="atualizar"),
    path("<int:empr>/<int:fili>/<int:codi>/excluir/", ContribuinteDeleteView.as_view(), name="deletar"),
]
