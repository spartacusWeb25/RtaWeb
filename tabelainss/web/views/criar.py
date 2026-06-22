from urllib.parse import urlencode

from django.views.generic import FormView
from django.urls import reverse
from django.shortcuts import redirect

from core.mixin import BancoObrigatorioMixin
from core.utils import format_month_reference
from tabelainss.web.forms import TabelainssForm
from tabelainss.services.criar import TabelaInssCriarService


class TabelainssCreateView(BancoObrigatorioMixin, FormView):
    template_name = "tabelainss/criar.html"
    form_class = TabelainssForm

    def form_valid(self, form):
        TabelaInssCriarService.criar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=form.cleaned_data,
        )

        return redirect(self.get_feedback_url(form.cleaned_data["tabe_refe"]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tabe_refe_salva = self.request.GET.get("salvo_ref", "").strip()
        context["mensagem_sucesso_form"] = ""
        context["redirect_delay_ms"] = 1800
        context["redirect_url"] = self.get_success_url()

        if tabe_refe_salva:
            context["mensagem_sucesso_form"] = (
                f"Referência {format_month_reference(tabe_refe_salva)} gravada com sucesso."
            )

        return context

    def get_success_url(self):
        return reverse("tabelainss:listar") + f"?banco={self.request.banco}"

    def get_feedback_url(self, tabe_refe):
        query = urlencode(
            {
                "banco": self.request.banco,
                "salvo_ref": tabe_refe,
            }
        )
        return f"{reverse('tabelainss:inss_criar')}?{query}"
