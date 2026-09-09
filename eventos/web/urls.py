from django.urls import path

from eventos.web.views.criar import EventoCreateView
from eventos.web.views.deletar import EventoDeleteView
from eventos.web.views.listar import EventosListView
from eventos.web.views.atualizar import EventoUpdateView

app_name = "eventos"

urlpatterns = [
    path("", EventosListView.as_view(), name="listar"),
    path("novo/", EventoCreateView.as_view(), name="criar"),
    path("<int:even_empr>/<int:even_codi>/editar/", EventoUpdateView.as_view(), name="atualizar"),
    path("<int:even_empr>/<int:even_codi>/excluir/", EventoDeleteView.as_view(), name="deletar"),
]