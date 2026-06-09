from django.views.generic import ListView
from core.mixin import BancoObrigatorioMixin
from ...models import Folhadecimo
from folhadecimo.services.listar import ListarFolhadDecimoService

class FolhadecimoListView(BancoObrigatorioMixin, ListView):
    model = Folhadecimo
    template_name = "folhadecimo/listar.html"
    context_object_name = "folhadecimo"
    paginate_by = 20
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarFolhadDecimoService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        