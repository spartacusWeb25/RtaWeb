from django.views.generic import ListView

from core.mixin import BancoObrigatorioMixin
from funcionarios.models import Funcionarios
from funcionarios.services import FuncionariosService


class FuncionarioListView(BancoObrigatorioMixin, ListView):
    model = Funcionarios
    template_name = "funcionarios/listar.html"
    context_object_name = "funcionarios"
    paginate_by = 20

    def get_queryset(self):
        return FuncionariosService.listar_por_banco(
            banco=self.request.banco,
            termo=self.request.GET.get("nome"),
        )
