from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View

from core.mixin import BancoObrigatorioMixin
from tabelairrf.services.excluir import TabelaIrrfExcluirService


class TabelairrfDeleteView(BancoObrigatorioMixin, View):
    def get_chave_dados(self):
        return {
            "irrf_refe": self.kwargs["irrf_refe"],
        }

    def post(self, request, *args, **kwargs):
        try:
            TabelaIrrfExcluirService.excluir(
                banco=request.banco,
                db_alias=request.db_alias,
                dados=self.get_chave_dados(),
            )
            messages.success(request, "Tabela IRRF removida com sucesso.")
        except ValueError as erro:
            messages.error(request, str(erro))

        return redirect(
            reverse("tabelairrf:listar") + f"?banco={request.banco}"
        )
