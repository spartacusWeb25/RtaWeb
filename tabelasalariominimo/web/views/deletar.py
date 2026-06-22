from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from core.mixin import BancoObrigatorioMixin
from tabelasalariominimo.services.excluir import SalarioMinimoExcluirService



class TabelasalariominimoDeleteView(BancoObrigatorioMixin, View):

    def get_chave_dados(self):
        return {
            "refe_sala_mini": self.kwargs["refe_sala_mini"],
        }

    def post(self, request, *args, **kwargs):
        try:
            SalarioMinimoExcluirService.excluir(   
                banco=request.banco,
                db_alias=request.db_alias,
                dados=self.get_chave_dados(),
            )
            messages.success(request, "Tabela salário mínimo removida com sucesso.")

        except ValueError as erro:
            messages.error(request, str(erro))

        return redirect(
            reverse("tabelasalariominimo:listar") + f"?banco={request.banco}"
        )
