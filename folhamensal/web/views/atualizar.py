from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import UpdateView

from core.mixin import BancoObrigatorioMixin
from folhamensal.models import Folhamensal
from folhamensal.services import FolhaMensalService
from folhamensal.web.forms import FolhaMensalForm


class FolhaMensalUpdateView(BancoObrigatorioMixin, UpdateView):
    model = Folhamensal
    form_class = FolhaMensalForm
    template_name = "folha/folha_mensal_form.html"

    def get_object(self, queryset=None):
        return get_object_or_404(
            Folhamensal,
            registro=self.request.banco,
            fome_func=self.kwargs["fome_func"],
            fome_refe=self.kwargs["fome_refe"],
            fome_even=self.kwargs["fome_even"],
        )

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.registro_id = self.request.banco
        FolhaMensalService.salvar(instance=instance)
        messages.success(self.request, "Lançamento atualizado com sucesso.")
        return redirect(reverse("folha:folha_mensal_listar") + f"?banco={self.request.banco}")
