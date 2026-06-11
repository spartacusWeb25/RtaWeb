from django.views.generic import ListView  
from core.mixin import BancoObrigatorioMixin, InfiniteScrollMixin
from ...models import Lancamentosfolha
from lancamentosfolha.services.listar import ListarLancamentosFolhaService          

class LancamentosfolhaListView(BancoObrigatorioMixin, InfiniteScrollMixin, ListView):
    model = Lancamentosfolha
    context_object_name = "lancamentosfolha"
    template_name = "lancamentosfolha/listar.html"
    paginate_by = 20   
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarLancamentosFolhaService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        
