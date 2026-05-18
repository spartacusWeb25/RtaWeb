from django.views.generic import ListView  
from core.mixin import BancoObrigatorioMixin
from ...models import Horarios
from horarios.services.listar import ListarHorariosService  

class HorarioListView(BancoObrigatorioMixin, ListView):
    model = Horarios
    context_object_name = "horarios"
    template_name = "horarios/listar.html"
    paginate_by = 20   
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarHorariosService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        
