from django.views.generic import ListView
from core.mixin import BancoObrigatorioMixin
from ...models import Ferias
from ferias.services.listar import ListarFeriasService

class FeriasListView(BancoObrigatorioMixin, ListView):
    model = Ferias
    template_name = "ferias/ferias_list.html"
    context_object_name = "ferias"
    paginate_by = 20
    
    def get_queryset(self):
        referencia = self.request.GET.get("ref")
        return ListarFeriasService.listar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            referencia=referencia,
        )
        