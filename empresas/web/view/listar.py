from django.views.generic import ListView
from core.mixin import BancoObrigatorioMixin
from ...models import Empresas
from empresas.services.listar import ListarEmpresasService

class EmpresasListView(BancoObrigatorioMixin, ListView):
    model = Empresas
    template_name = "empresas/empresas_list.html"
    context_object_name = "empresas"
    paginate_by = 20
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarEmpresasService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        