from django.views.generic import ListView  

from core.mixin import BancoObrigatorioMixin
from ...models import Funcionarios
from funcionarios.services.listar import ListarFuncionariosService   


class FuncionarioListView(BancoObrigatorioMixin, ListView):
    model = Funcionarios
    context_object_name = "funcionarios"
    template_name = "funcionarios/listar.html"
    paginate_by = 20   
    
    def get_queryset(self):
        referencia = self.request.GET.get("nome") or self.request.GET.get("ref")
        return ListarFuncionariosService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
