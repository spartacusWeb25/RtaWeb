from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.mixin import BancoObrigatorioMixin
from contribuintes.models import Contribuintes
from contribuintes.services.logic import ContribuintesService


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


class ContribuinteDeleteView(BancoObrigatorioMixin, TemplateView):
    template_name = "contribuintes/confirmar_exclusao.html"

    def get_contribuinte(self):
        banco_limpo = _digits_only(self.request.banco)
        contribuinte = (
            self.get_queryset()
            .filter(
                registro=banco_limpo,
                contr_empr=self.kwargs["empr"],
                contr_fili=self.kwargs["fili"],
                contr_codi=self.kwargs["codi"],
            )
            .first()
        )
        if contribuinte is None:
            raise Http404
        return contribuinte

    def get_queryset(self):
        banco_limpo = _digits_only(self.request.banco)
        return Contribuintes.objects.using(self.request.db_alias).filter(
            registro=banco_limpo
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_contribuinte()
        context["object"] = obj
        context["contribuinte"] = obj
        return context

    def post(self, request, *args, **kwargs):
        banco_limpo = _digits_only(request.banco)
        contribuinte = self.get_contribuinte()
        ContribuintesService.excluir_contribuinte(
            contribuinte,
            request.db_alias,
        )
        messages.success(request, "Contribuinte excluído com sucesso.")
        return redirect(reverse("contribuintes:listar") + f"?banco={banco_limpo}")
