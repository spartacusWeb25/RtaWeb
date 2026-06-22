from urllib.parse import urlencode

from django.views.generic import FormView
from django.urls import reverse
from django.shortcuts import redirect

from core.mixin import BancoObrigatorioMixin
from core.utils import format_month_reference
from tabelasalariominimo.web.forms import TabelasalariominimoForm
from tabelasalariominimo.services.criar import TabelaSalarioMinimoCriarService


class TabelasalariominimoCreateView(BancoObrigatorioMixin, FormView):
    template_name = "tabelasalariominimo/criar.html"
    form_class = TabelasalariominimoForm

    def form_valid(self, form):
        TabelaSalarioMinimoCriarService.criar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=form.cleaned_data,
        )

        return redirect(self.get_feedback_url(form.cleaned_data["refe_sala_mini"]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        refe_sala_mini_salva = self.request.GET.get("salvo_ref", "").strip()
        context["mensagem_sucesso_form"] = ""
        context["redirect_delay_ms"] = 1800
        context["redirect_url"] = self.get_success_url()

        if refe_sala_mini_salva:
            context["mensagem_sucesso_form"] = (
                f"Referência {format_month_reference(refe_sala_mini_salva)} gravada com sucesso."
            )

        return context

    def get_success_url(self):
        return reverse("tabelasalariominimo:listar") + f"?banco={self.request.banco}"

    def get_feedback_url(self, refe_sala_mini):
        query = urlencode(
            {
                "banco": self.request.banco,
                "salvo_ref": refe_sala_mini,
            }
        )
        return f"{reverse('tabelasalariominimo:salariominimo_criar')}?{query}"
