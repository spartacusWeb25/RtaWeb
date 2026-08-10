from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from core.mixin import BancoObrigatorioMixin
from dependentesrh.services.excluir import DependentesExcluirService
from dependentesrh.services.chave import DependentesChaveService
from dependentesrh.web.views.criar import _obter_contexto_funcionario


class DependentesrhDeleteView(BancoObrigatorioMixin, View):

    def get_chave_dados(self):
        return {
            "depe_empr": self.kwargs["empresa"],
            "depe_fili": self.kwargs["filial"],
            "depe_func": self.kwargs["funcionario"],
            "depe_codi": self.kwargs["codigo"],
        }

    def _base_sucesso_url(self, request):
        empr = self.kwargs["empresa"]
        fili = self.kwargs["filial"]
        func = self.kwargs["funcionario"]
        if func and empr and fili:
            try:
                return (
                    reverse(
                        "funcionarios:atualizar",
                        kwargs={
                            "func_empr": int(empr),
                            "func_fili": int(fili),
                            "func_codi": int(func),
                        },
                    )
                    + f"?banco={request.banco}#tab-parentes"
                )
            except Exception:
                pass
        return reverse("dependentesrh:listar") + f"?banco={request.banco}"

    def get(self, request, *args, **kwargs):
        from django.shortcuts import render

        dependente = DependentesChaveService.buscar(
            banco=request.banco,
            db_alias=request.db_alias,
            dados=self.get_chave_dados(),
        )
        context = {
            "objeto": self.get_chave_dados(),
            "objeto_nome": (
                dependente.depe_nome if dependente else f"Dependente #{self.kwargs['codigo']}"
            ),
            "dependente": dependente,
            "funcionario_contexto": _obter_contexto_funcionario(
                request,
                self.kwargs["empresa"],
                self.kwargs["filial"],
                self.kwargs["funcionario"],
            ),
            "url_voltar": self._base_sucesso_url(request),
        }
        return render(request, "dependentesrh/confirmar_exclusao.html", context)

    def post(self, request, *args, **kwargs):
        try:
            DependentesExcluirService.excluir(
                banco=request.banco,
                db_alias=request.db_alias,
                dados=self.get_chave_dados(),
            )
            messages.success(request, "Dependente removido com sucesso.")

        except ValueError as erro:
            messages.error(request, str(erro))

        return redirect(self._base_sucesso_url(request))
