from django.urls import path

from funcionarios.web.views.criar import FuncionarioCreateView
from funcionarios.web.views.deletar import FuncionarioDeleteView
from funcionarios.web.views.listar import FuncionarioListView
from funcionarios.web.views.atualizar import FuncionarioUpdateView

app_name = "funcionarios"

urlpatterns = [
    path("", FuncionarioListView.as_view(), name="listar"),
    path("novo/", FuncionarioCreateView.as_view(), name="criar"),
    path("<int:func_codi>/editar/", FuncionarioUpdateView.as_view(), name="atualizar"),
    path("<int:func_codi>/excluir/", FuncionarioDeleteView.as_view(), name="deletar"),
]
