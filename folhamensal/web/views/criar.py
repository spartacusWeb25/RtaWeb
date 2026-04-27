from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from core.mixin import BancoObrigatorioMixin
from folhamensal.models import Folhamensal
from folhamensal.services import FolhaMensalService
from folhamensal.web.forms import FolhaMensalForm


class FolhaMensalCreateView(BancoObrigatorioMixin, CreateView):
    model = Folhamensal
    form_class = FolhaMensalForm
    template_name = "folha/folha_mensal_form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.registro_id = self.request.banco
        FolhaMensalService.salvar(instance=instance)
        messages.success(self.request, "Lançamento criado com sucesso.")
        return redirect(reverse("folha:folha_mensal_listar") + f"?banco={self.request.banco}")
