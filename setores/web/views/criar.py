from django.views.generic import FormView
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect

from core.mixin import BancoObrigatorioMixin
from setores.web.forms import SetoresrhForm
from setores.services.criar import SetoresCriarService


class SetoresCreateView(BancoObrigatorioMixin, FormView):
    template_name = "setores/criar.html"
    form_class = SetoresrhForm

    def form_valid(self, form):
        SetoresCriarService.criar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=form.cleaned_data,
        )

        messages.success(self.request, "Setor criado com sucesso.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("setores:setoresrh_listar") + f"?banco={self.request.banco}"