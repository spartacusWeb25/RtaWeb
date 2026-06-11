from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from core.mixin import BancoObrigatorioMixin
from tabelasalafami.services.excluir import SalaFamiExcluirService



class TabelasalafamiDeleteView(BancoObrigatorioMixin, View):

    def get_chave_dados(self):
        return {
            "safa_refe": self.kwargs["safa_refe"],
        }

    def post(self, request, *args, **kwargs):
        try:
            SalaFamiExcluirService.excluir(   
                banco=request.banco,
                db_alias=request.db_alias,
                dados=self.get_chave_dados(),
            )
            messages.success(request, "Tabelasalafami removido com sucesso.")

        except ValueError as erro:
            messages.error(request, str(erro))

        return redirect(
            reverse("tabelasalafami:tabelasalafami_listar") + f"?banco={request.banco}"
        )