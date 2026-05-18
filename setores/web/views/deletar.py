from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from core.mixin import BancoObrigatorioMixin
from setores.services.excluir import SetoresExcluirService



class SetoresrhDeleteView(BancoObrigatorioMixin, View):

    def get_chave_dados(self):
        return {
            "seto_empr": self.kwargs["empresa"],
            "seto_codi": self.kwargs["codigo"],
        }

    def post(self, request, *args, **kwargs):
        try:
            SetoresExcluirService.excluir(
                banco=request.banco,
                db_alias=request.db_alias,
                dados=self.get_chave_dados(),
            )
            messages.success(request, "Setor removido com sucesso.")

        except ValueError as erro:
            messages.error(request, str(erro))

        return redirect(
            reverse("setores:setoresrh_listar") + f"?banco={request.banco}"
        )