from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.mixin import BancoObrigatorioMixin
from folhamensal.models import Folhamensal
from folhamensal.services import FolhaMensalService


class FolhaMensalDeleteView(BancoObrigatorioMixin, TemplateView):
    template_name = "folha/folha_mensal_confirmar_exclusao.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = get_object_or_404(
            Folhamensal,
            registro=self.request.banco,
            fome_func=self.kwargs["fome_func"],
            fome_refe=self.kwargs["fome_refe"],
            fome_even=self.kwargs["fome_even"],
        )
        return context

    def post(self, request, *args, **kwargs):
        item = get_object_or_404(
            Folhamensal,
            registro=request.banco,
            fome_func=kwargs["fome_func"],
            fome_refe=kwargs["fome_refe"],
            fome_even=kwargs["fome_even"],
        )
        FolhaMensalService.remover(instance=item)
        messages.success(request, "Lançamento excluído com sucesso.")
        return redirect(reverse("folha:folha_mensal_listar") + f"?banco={request.banco}")
