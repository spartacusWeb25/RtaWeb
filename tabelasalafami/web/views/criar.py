from django.views.generic import FormView
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect

from core.mixin import BancoObrigatorioMixin
from tabelasalafami.web.forms import TabelasalafamiForm
from tabelasalafami.services.criar import SalaFamiCriarService


class TabelasalafamiCreateView(BancoObrigatorioMixin, FormView):
    template_name = "tabelasalafami/criar.html"
    form_class = TabelasalafamiForm

    def form_valid(self, form):
        SalaFamiCriarService.criar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=form.cleaned_data,
        )

        messages.success(self.request, "Salário familia criado com sucesso.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("tabelasalafami:salafami_listar") + f"?banco={self.request.banco}"
