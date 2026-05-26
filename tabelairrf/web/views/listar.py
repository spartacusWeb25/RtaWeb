from django.views.generic import ListView  
from core.mixin import BancoObrigatorioMixin
from ...models import Tabelairrf
from tabelairrf.services.listar import ListarTabelairrfService     
       
class TabelairrfListView(BancoObrigatorioMixin, ListView):
    model = Tabelairrf
    context_object_name = "tabelairrf"
    template_name = "tabelairrf/listar.html"
    paginate_by = 20   
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarTabelairrfService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        