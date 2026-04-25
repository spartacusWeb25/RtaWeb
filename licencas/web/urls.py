from django.urls import path

from licencas.web.views.atualizar import UsuarioLicencaUpdateView
from licencas.web.views.criar import UsuarioLicencaCreateView
from licencas.web.views.deletar import UsuarioLicencaDeleteView
from licencas.web.views.listar import UsuarioLicencaListView

app_name = "usuarios"

urlpatterns = [
    path("", UsuarioLicencaListView.as_view(), name="listar"),
    path("novo/", UsuarioLicencaCreateView.as_view(), name="criar"),
    path("<int:user_id>/editar/", UsuarioLicencaUpdateView.as_view(), name="atualizar"),
    path("<int:user_id>/excluir/", UsuarioLicencaDeleteView.as_view(), name="deletar"),
]
