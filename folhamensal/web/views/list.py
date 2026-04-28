from django.views.generic import ListView

from core.mixin import BancoObrigatorioMixin
from folhamensal.models import Folhamensal
from folhamensal.services.folha_mensal import FolhaMensal


class FolhaMensalListView(BancoObrigatorioMixin, ListView):
    model = Folhamensal
    template_name = "folha/folha_mensal_listar.html"
    context_object_name = "folhas"
    paginate_by = 25

    def get_queryset(self):
        # A conferência consome os dados em `dados` via serviço SQL consolidado.
        return Folhamensal.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        empresa = self.request.GET.get("empresa")
        filial = self.request.GET.get("filial")
        referencia = self.request.GET.get("referencia")
        funcionario = self.request.GET.get("funcionario")

        dados = []
        totais = None

        if empresa and referencia:
            dados = FolhaMensal.conferencia_tributos(
                db_alias=self.request.db_alias,
                registro=self.request.banco,
                empresa=int(empresa),
                filial=int(filial) if filial else None,
                referencia=referencia,
                funcionario=int(funcionario) if funcionario else None,
            )
            totais = FolhaMensal.totais_gerais(dados)

        context["dados"] = dados
        context["totais"] = totais
        return context
