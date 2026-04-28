from django.views.generic import ListView

from core.mixin import BancoObrigatorioMixin
from tabelas.models import Tabelainss, Tabelainssempresa, Tabelairrf
from tabelas.services.service_tabela_inss import ServiceTabelaInss
from tabelas.services.service_tabela_inss_empresa import ServiceTabelaInssEmpresa
from tabelas.services.service_tabela_irrf import ServiceTabelaIrf


class TabelaIrrfListView(BancoObrigatorioMixin, ListView):
    model = Tabelairrf
    template_name = "tabelas/irrf_list.html"
    context_object_name = "tabelas"
    paginate_by = 20

    def get_queryset(self):
        referencia = self.request.GET.get("ref")

        return ServiceTabelaIrf.buscar_tabela_irrf_queryset(
            db_alias=self.request.db_alias,
            referencia=referencia,
        )


class TabelaInssListView(BancoObrigatorioMixin, ListView):
    model = Tabelainss
    template_name = "tabelas/inss_list.html"
    context_object_name = "tabelas"
    paginate_by = 20

    def get_queryset(self):
        referencia = self.request.GET.get("ref")

        return ServiceTabelaInss.buscar_tabela_inss_queryset(
            db_alias=self.request.db_alias,
            referencia=referencia,
        )


class TabelaInssEmpresaListView(BancoObrigatorioMixin, ListView):
    model = Tabelainssempresa
    template_name = "tabelas/inss_empresa_list.html"
    context_object_name = "tabelas"
    paginate_by = 20

    def get_queryset(self):
        return ServiceTabelaInssEmpresa.buscar_tabela_inss_empresa_queryset(
            db_alias=self.request.db_alias,
            registro=self.request.banco,
        )
