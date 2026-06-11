from django.views.generic import ListView

from core.mixin import BancoObrigatorioMixin, InfiniteScrollMixin
from ...models import Dadosrescisao
from dadosrescisao.services.listar import ListarDadosRescisaoService

class DadosRescisaoListView(BancoObrigatorioMixin, InfiniteScrollMixin, ListView):
    model = Dadosrescisao
    template_name = "dadosrescisao/listar.html"
    context_object_name = "dadosrescisaos"
    paginate_by = 20
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarDadosRescisaoService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        
