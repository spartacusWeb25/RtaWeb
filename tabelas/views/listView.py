from django.views.generic import ListView
from tabelas.models import Tabelairrf
from ..services.service_tabela_irrf import ServiceTabelaIrf


class TabelaIrrfListView(ListView):
    model = Tabelairrf
    template_name = "tabelas/irrf_list.html"
    context_object_name = "tabelas"
    paginate_by = 20

    def get_queryset(self):
        db_alias = self.request.GET.get("db", "default")
        referencia = self.request.GET.get("ref")

        return ServiceTabelaIrf.buscar_tabela_irrf_queryset(
            db_alias=db_alias,
            referencia=referencia
        )