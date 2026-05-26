from django.views.generic import ListView  
from core.mixin import BancoObrigatorioMixin
from ...models import Sindicatos
from sindicatos.services.listar import ListarSindicatosService          

class SindicatoListView(BancoObrigatorioMixin, ListView):
    model = Sindicatos
    context_object_name = "sindicatos"
    template_name = "sindicatos/listar.html"
    paginate_by = 20   
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarSindicatosService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        
