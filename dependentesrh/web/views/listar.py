from django.views.generic import ListView

from core.mixin import BancoObrigatorioMixin
from ...models import Dependentesrh
from dependentesrh.services.listar import ListarDependentesRhService

class DependentesRhListView(BancoObrigatorioMixin, ListView):
    model = Dependentesrh
    template_name = "dependentesrh/listar.html"
    context_object_name = "dependentesrh"
    paginate_by = 20
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarDependentesRhService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        