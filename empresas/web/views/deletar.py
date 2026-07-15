from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View

from core.banco import get_banco_from_request
from core.mixin import BancoObrigatorioMixin
from core.utils import get_db_from_slug
from empresas.services.excluir import EmpresaExcluirService


class EmpresasDeleteView(BancoObrigatorioMixin, View):
    def get_chave_dados(self):
        return {
            "registro": self.request.banco,
            "empr_empr": self.kwargs["empresa"],
            "empr_fili": self.kwargs["filial"],
        }

    def post(self, request, *args, **kwargs):
        request.banco = getattr(request, "banco", None) or get_banco_from_request(request)
        if not request.banco:
            messages.error(request, "Banco da licença não informado.")
            return redirect(reverse("empresas:listar"))

        request.db_alias = get_db_from_slug(request.banco)
        try:
            EmpresaExcluirService.excluir(
                banco=request.banco,
                db_alias=request.db_alias,
                dados=self.get_chave_dados(),
            )
            messages.success(request, "Empresa removida com sucesso.")
        except ValueError as erro:
            messages.error(request, str(erro))

        return redirect(
            reverse("empresas:listar") + f"?banco={request.banco}"
        )
