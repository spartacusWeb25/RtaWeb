from django.views.generic import ListView  
from core.mixin import BancoObrigatorioMixin
from ...models import Tabelasalafami
from tabelasalafami.services.listar import ListarTabelasalafamiService     
        
class TabelasalafamiListView(BancoObrigatorioMixin, ListView):
    model = Tabelasalafami
    context_object_name = "tabelasalafami"
    template_name = "tabelasalafami/listar.html"
    paginate_by = 20   
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarTabelasalafamiService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        