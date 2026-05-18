from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView

from core.mixin import BancoObrigatorioMixin
from folhamensal.models import Folhamensal
from folhamensal.services import FolhaMensalEditarService
from folhamensal.web.forms import FolhaMensalForm


class FolhaMensalUpdateView(BancoObrigatorioMixin, UpdateView):
    model = Folhamensal
    form_class = FolhaMensalForm
    template_name = "folha/folha_mensal_form.html"

    def get_object(self, queryset=None):
        return FolhaMensalEditarService.buscar_unico(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            fome_empr=self.kwargs["fome_empr"],
            fome_fili=self.kwargs["fome_fili"],
            fome_func=self.kwargs["fome_func"],
            fome_refe=self.kwargs["fome_refe"],
            fome_even=self.kwargs["fome_even"],
        )

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.registro_id = self.request.banco
        FolhaMensalEditarService.editar(instance=instance, db_alias=self.request.db_alias)
        messages.success(self.request, "Lançamento atualizado com sucesso.")
        return redirect(reverse("folha:folha_mensal_listar") + f"?banco={self.request.banco}")
