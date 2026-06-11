from django.views.generic import ListView   
from core.mixin import BancoObrigatorioMixin, InfiniteScrollMixin
from ...models import Folhaquinzenal
from folhaquinzenal.services.listar import ListarFolhaQuinzenalService

class FolhaQuinzenalListView(BancoObrigatorioMixin, InfiniteScrollMixin, ListView):
    model = Folhaquinzenal
    context_object_name = "folhaquinzenal"
    template_name = "folhaquinzenal/listar.html"
    paginate_by = 20    

    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarFolhaQuinzenalService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
    
