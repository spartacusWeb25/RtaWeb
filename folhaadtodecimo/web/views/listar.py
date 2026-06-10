from django.views.generic import ListView
from core.mixin import BancoObrigatorioMixin
from ...models import Folhaadtodecimo
from folhaadtodecimo.services.listar import ListarFolhaAdtodecimoService

class FolhaAdtodecimoListView(BancoObrigatorioMixin, ListView):
    model = Folhaadtodecimo
    template_name = "folhaadtodecimo/listar.html"
    context_object_name = "folhaadtodecimo"
    paginate_by = 20
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarFolhaAdtodecimoService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        