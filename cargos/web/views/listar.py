from django.views.generic import ListView

from core.mixin import BancoObrigatorioMixin, InfiniteScrollMixin
from ...models import Cargos
from cargos.services.listar import ListarCargosService

class CargosListView(BancoObrigatorioMixin, InfiniteScrollMixin, ListView):
    model = Cargos
    template_name = "cargos/listar.html"
    context_object_name = "cargos"
    paginate_by = 20
    
    def get_queryset(self):
        referencia = self.request.GET.get("referencia")
        return ListarCargosService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        
