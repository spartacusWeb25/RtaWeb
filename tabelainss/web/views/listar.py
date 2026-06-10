from django.views.generic import ListView  

from core.mixin import BancoObrigatorioMixin, InfiniteScrollMixin
from ...models import Tabelainss
from tabelainss.services.listar import ListarTabelainssService     


class TabelainssListView(BancoObrigatorioMixin, InfiniteScrollMixin, ListView):
    model = Tabelainss
    context_object_name = "tabelainss"
    template_name = "tabelainss/listar.html"
    paginate_by = 20   
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarTabelainssService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        
