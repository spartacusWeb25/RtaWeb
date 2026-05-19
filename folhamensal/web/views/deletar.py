from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.mixin import BancoObrigatorioMixin
from folhamensal.services.remover_por_chave import FolhaMensalRemoverService

class FolhaMensalDeleteView(BancoObrigatorioMixin, TemplateView):
    template_name = "folha/folha_mensal_confirmar_exclusao.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["item"] = FolhaMensalRemoverService.buscar_por_chave(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            fome_empr=self.kwargs["fome_empr"],
            fome_fili=self.kwargs["fome_fili"],
            fome_func=self.kwargs["fome_func"],
            fome_refe=self.kwargs["fome_refe"],
            fome_even=self.kwargs["fome_even"],
        )

        return context

    def post(self, request, *args, **kwargs):
        FolhaMensalRemoverService.remover_por_chave(
            banco=request.banco,
            db_alias=request.db_alias,
            fome_empr=kwargs["fome_empr"],
            fome_fili=kwargs["fome_fili"],
            fome_func=kwargs["fome_func"],
            fome_refe=kwargs["fome_refe"],
            fome_even=kwargs["fome_even"],
        )

        messages.success(request, "Lançamento excluído com sucesso.")
        return redirect(reverse("folha:folha_mensal_listar") + f"?banco={request.banco}")