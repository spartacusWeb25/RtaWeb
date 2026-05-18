from django.views.generic import ListView

from core.mixin import BancoObrigatorioMixin
from ...models import Adtodecimo
from adtodecimo.services.listar import ListarAdtoDecimoService


class AdtodecimoListView(BancoObrigatorioMixin, ListView):
    model = Adtodecimo
    template_name = "adtodecimo/adtodecimo_list.html"
    context_object_name = "adtodecimos"
    paginate_by = 20
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarAdtoDecimoService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )