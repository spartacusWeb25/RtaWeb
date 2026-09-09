from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from core.mixin import BancoObrigatorioMixin
from dependentescontr.services.excluir import DependentescontrExcluirService
from dependentescontr.services.chave import DependentescontrChaveService
from dependentescontr.web.views.criar import _obter_contexto_contribuinte, _digits_only


class DependentescontrDeleteView(BancoObrigatorioMixin, View):

    def get_chave_dados(self):
        return {
            "depecontr_empr": self.kwargs["empr"],
            "depecontr_fili": self.kwargs["fili"],
            "depecontr_contr": self.kwargs["contr"],
            "depecontr_codi": self.kwargs["codi"],
        }

    def _base_sucesso_url(self, request):
        banco_limpo = _digits_only(request.banco)
        empr = self.kwargs["empr"]
        fili = self.kwargs["fili"]
        contr = self.kwargs["contr"]
        if contr and empr and fili:
            try:
                return (
                    reverse(
                        "contribuintes:atualizar",
                        kwargs={
                            "empr": int(empr),
                            "fili": int(fili),
                            "codi": int(contr),
                        },
                    )
                    + f"?banco={banco_limpo}#tab-dependentes"
                )
            except Exception:
                pass
        return reverse("contribuintes:listar") + f"?banco={banco_limpo}"

    def get(self, request, *args, **kwargs):
        from django.shortcuts import render
        banco_limpo = _digits_only(request.banco)

        dependente = DependentescontrChaveService.buscar(
            banco=banco_limpo,
            db_alias=request.db_alias,
            dados=self.get_chave_dados(),
        )
        context = {
            "objeto": self.get_chave_dados(),
            "objeto_nome": (
                dependente.depecontr_nome if dependente else f"Dependente #{self.kwargs['codi']}"
            ),
            "dependente": dependente,
            "contribuinte_contexto": _obter_contexto_contribuinte(
                request,
                self.kwargs["empr"],
                self.kwargs["fili"],
                self.kwargs["contr"],
            ),
            "url_voltar": self._base_sucesso_url(request),
        }
        return render(request, "dependentescontr/confirmar_exclusao.html", context)

    def post(self, request, *args, **kwargs):
        banco_limpo = _digits_only(request.banco)
        try:
            DependentescontrExcluirService.excluir(
                banco=banco_limpo,
                db_alias=request.db_alias,
                dados=self.get_chave_dados(),
            )
            messages.success(request, "Dependente de contribuinte removido com sucesso.")

        except ValueError as erro:
            messages.error(request, str(erro))

        return redirect(self._base_sucesso_url(request))
