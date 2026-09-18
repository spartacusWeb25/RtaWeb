from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.mixin import BancoObrigatorioMixin
from terceiros.models import Terceiros
from terceiros.services.logic import TerceirosService


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


class TerceiroDeleteView(BancoObrigatorioMixin, TemplateView):
    template_name = "terceiros/confirmar_exclusao.html"

    def get_terceiro(self):
        banco_limpo = _digits_only(self.request.banco)
        terceiro = (
            self.get_queryset()
            .filter(
                registro=banco_limpo,
                terc_empr=self.kwargs["empr"],
                terc_fili=self.kwargs["fili"],
                terc_codi=self.kwargs["codi"],
            )
            .first()
        )
        if terceiro is None:
            raise Http404
        return terceiro

    def get_queryset(self):
        banco_limpo = _digits_only(self.request.banco)
        return Terceiros.objects.using(self.request.db_alias).filter(
            registro=banco_limpo
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_terceiro()
        context["object"] = obj
        context["terceiro"] = obj
        return context

    def post(self, request, *args, **kwargs):
        banco_limpo = _digits_only(request.banco)
        terceiro = self.get_terceiro()
        TerceirosService.excluir_terceiro(
            terceiro,
            request.db_alias,
        )
        messages.success(request, "Terceiro excluído com sucesso.")
        return redirect(reverse("terceiros:listar") + f"?banco={banco_limpo}")
