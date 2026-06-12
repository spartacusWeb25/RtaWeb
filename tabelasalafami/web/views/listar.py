from django.views.generic import ListView  
from core.mixin import BancoObrigatorioMixin, InfiniteScrollMixin
from ...models import Tabelasalafami
from tabelasalafami.services.listar import ListarTabelasalafamiService     
        
class TabelasalafamiListView(BancoObrigatorioMixin, InfiniteScrollMixin, ListView):
    model = Tabelasalafami
    context_object_name = "tabelasalafami"
    template_name = "tabelasalafami/listar.html"
    paginate_by = 20   
    
    def get_queryset(self):
        referencia = (self.request.GET.get("referencia") or "").strip()
        ordenar = self.request.GET.get("ordenar") or ""

        return ListarTabelasalafamiService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
            ordenar=ordenar,
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["referencia"] = (self.request.GET.get("referencia") or "").strip()
        context["ordenar"] = self.request.GET.get("ordenar") or ""
        return context
