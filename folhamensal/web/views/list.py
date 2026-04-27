from django.views.generic import ListView

from core.mixin import BancoObrigatorioMixin
from folhamensal.models import Folhamensal
from folhamensal.services.folha_mensal import FolhaMensal



class FolhaMensalListView(BancoObrigatorioMixin, ListView):
    model = Folhamensal
    template_name = "folha/folha_mensal_list.html"
    context_object_name = "folhas"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        empresa = self.request.GET.get("empresa")
        filial = self.request.GET.get("filial")
        referencia = self.request.GET.get("referencia")
        nome = self.request.GET.get("nome")

        dados = []
        totais = None

        if empresa and referencia:
            dados = FolhaMensal.conferencia_tributos(
                db_alias=self.request.db_alias,
                registro=self.request.banco,
                empresa=int(empresa),
                filial=int(filial) if filial else None,
                referencia=referencia,

            )

            totais = FolhaMensal.totais_gerais(dados)

        context["dados"] = dados
        context["totais"] = totais
        return context
