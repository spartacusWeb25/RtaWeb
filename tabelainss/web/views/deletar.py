from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from core.mixin import BancoObrigatorioMixin
from tabelainss.services.excluir import TabelaInssExcluirService



class TabelainssDeleteView(BancoObrigatorioMixin, View):

    def get_chave_dados(self):
        return {
            "tabe_refe": self.kwargs["tabe_refe"],
        }

    def post(self, request, *args, **kwargs):
        try:
            TabelaInssExcluirService.excluir(   
                banco=request.banco,
                db_alias=request.db_alias,
                dados=self.get_chave_dados(),
            )
            messages.success(request, "Tabela inss removida com sucesso.")

        except ValueError as erro:
            messages.error(request, str(erro))

        return redirect(
            reverse("tabelainss:listar") + f"?banco={request.banco}"
        )
