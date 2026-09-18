from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from core.mixin import BancoObrigatorioMixin
from dependentesterc.services.excluir import DependentestercExcluirService
from dependentesterc.services.chave import DependentestercChaveService
from dependentesterc.web.views.criar import _obter_contexto_terceiro, _digits_only


class DependentestercDeleteView(BancoObrigatorioMixin, View):

    def get_chave_dados(self):
        return {
            "depe_empr": self.kwargs["empr"],
            "depe_fili": self.kwargs["fili"],
            "depe_terc": self.kwargs["terc"],
            "depe_codi": self.kwargs["codi"],
        }

    def _base_sucesso_url(self, request):
        banco_limpo = _digits_only(request.banco)
        empr = self.kwargs["empr"]
        fili = self.kwargs["fili"]
        terc = self.kwargs["terc"]
        if terc and empr and fili:
            try:
                return (
                    reverse(
                        "terceiros:atualizar",
                        kwargs={
                            "empr": int(empr),
                            "fili": int(fili),
                            "codi": int(terc),
                        },
                    )
                    + f"?banco={banco_limpo}#tab-dependentes"
                )
            except Exception:
                pass
        return reverse("terceiros:listar") + f"?banco={banco_limpo}"

    def get(self, request, *args, **kwargs):
        banco_limpo = _digits_only(request.banco)

        obj = DependentestercChaveService.buscar(
            banco=banco_limpo,
            db_alias=request.db_alias,
            dados=self.get_chave_dados(),
        )
        context = {
            "object": obj if obj else self.get_chave_dados(),
            "objeto_nome": (
                obj.depe_nome if obj else f"Dependente #{self.kwargs['codi']}"
            ),
            "objeto": obj,
            "dependente": obj,
            "banco_limpo": banco_limpo,
            "terceiro_contexto": _obter_contexto_terceiro(
                request,
                self.kwargs["empr"],
                self.kwargs["fili"],
                self.kwargs["terc"],
            ),
            "url_voltar": self._base_sucesso_url(request),
        }
        return render(request, "dependentesterc/confirmar_exclusao.html", context)

    def post(self, request, *args, **kwargs):
        banco_limpo = _digits_only(request.banco)
        try:
            DependentestercExcluirService.excluir(
                banco=banco_limpo,
                db_alias=request.db_alias,
                dados=self.get_chave_dados(),
            )
            messages.success(request, "Dependente de terceiro removido com sucesso.")

        except ValueError as erro:
            messages.error(request, str(erro))

        return redirect(self._base_sucesso_url(request))
