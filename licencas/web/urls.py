from django.urls import path

from licencas.web.views.atualizar import UsuariosUpdateView
from licencas.web.views.criar import UsuariosCreateView
from licencas.web.views.deletar import UsuariosDeleteView
from licencas.web.views.listar import UsuariosListView

app_name = "licencas"

urlpatterns = [
    path("listar/", UsuariosListView.as_view(), name="listar"),
    path("novo/", UsuariosCreateView.as_view(), name="criar"),
    path("<int:user_id>/editar/", UsuariosUpdateView.as_view(), name="atualizar"),
    path("<int:user_id>/excluir/", UsuariosDeleteView.as_view(), name="deletar"),
]
