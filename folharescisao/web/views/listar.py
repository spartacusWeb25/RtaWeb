from django.views.generic import ListView  

from core.mixin import BancoObrigatorioMixin, InfiniteScrollMixin
from ...models import Folharescisao
from folharescisao.services.listar import ListarFolhaRescisaoService


class FolhaRescisaoListView(BancoObrigatorioMixin, InfiniteScrollMixin, ListView):
    model = Folharescisao
    context_object_name = "folharescisao"
    template_name = "folharescisao/listar.html"
    paginate_by = 20   
     
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarFolhaRescisaoService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
