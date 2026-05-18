from django.views.generic import ListView  
from core.mixin import BancoObrigatorioMixin
from ...models import Tabelasalarial
from tabelasalarial.services.listar import ListarTabelasalarialService     
        
class TabelasalarialListView(BancoObrigatorioMixin, ListView):
    model = Tabelasalarial
    context_object_name = "tabelasalarial"
    template_name = "tabelasalarial/listar.html"
    paginate_by = 20   
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarTabelasalarialService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        