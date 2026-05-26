from django.views.generic import ListView  
from core.mixin import BancoObrigatorioMixin
from ...models import Tabelasalariominimo
from tabelasalariominimo.services.listar import ListarTabelasalariominimoService     
        
class TabelasalariominimoListView(BancoObrigatorioMixin, ListView):
    model = Tabelasalariominimo
    context_object_name = "tabelasalariominimo"
    template_name = "tabelasalariominimo/listar.html"
    paginate_by = 20   
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarTabelasalariominimoService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        