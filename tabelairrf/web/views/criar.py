from urllib.parse import urlencode

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from core.mixin import BancoObrigatorioMixin
from core.utils import format_month_reference
from tabelairrf.services.criar import TabelaIrrfCriarService
from tabelairrf.web.forms import TabelairrfForm


class TabelairrfCreateView(BancoObrigatorioMixin, FormView):
    template_name = "tabelairrf/criar.html"
    form_class = TabelairrfForm

    def form_valid(self, form):
        TabelaIrrfCriarService.criar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=form.cleaned_data,
        )

        return redirect(self.get_feedback_url(form.cleaned_data["irrf_refe"]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        irrf_refe_salva = self.request.GET.get("salvo_ref", "").strip()
        context["mensagem_sucesso_form"] = ""
        context["redirect_delay_ms"] = 1800
        context["redirect_url"] = self.get_success_url()

        if irrf_refe_salva:
            context["mensagem_sucesso_form"] = (
                f"Referência {format_month_reference(irrf_refe_salva)} gravada com sucesso."
            )

        return context

    def get_success_url(self):
        return reverse("tabelairrf:listar") + f"?banco={self.request.banco}"

    def get_feedback_url(self, irrf_refe):
        query = urlencode(
            {
                "banco": self.request.banco,
                "salvo_ref": irrf_refe,
            }
        )
        return f"{reverse('tabelairrf:irrf_criar')}?{query}"
