from django.views.generic import ListView

from core.mixin import BancoObrigatorioMixin, InfiniteScrollMixin
from ...models import Afastamentos
from afastamentos.services.listar import ListarAfastamentosService

class AfastamentosListView(BancoObrigatorioMixin, InfiniteScrollMixin, ListView):
    model = Afastamentos
    template_name = "afastamentos/listar.html"
    context_object_name = "afastamentos"
    paginate_by = 20
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarAfastamentosService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
