from urllib.parse import urlencode

from django.views.generic import FormView
from django.urls import reverse
from django.shortcuts import redirect

from core.mixin import BancoObrigatorioMixin
from core.utils import format_month_reference
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

        return redirect(self.get_feedback_url(form.cleaned_data["safa_refe"]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        safa_refe_salva = self.request.GET.get("salvo_ref", "").strip()
        context["mensagem_sucesso_form"] = ""
        context["redirect_delay_ms"] = 1800
        context["redirect_url"] = self.get_success_url()

        if safa_refe_salva:
            context["mensagem_sucesso_form"] = (
                f"Referência {format_month_reference(safa_refe_salva)} gravada com sucesso."
            )

        return context

    def get_success_url(self):
        return reverse("tabelasalafami:salafami_listar") + f"?banco={self.request.banco}"

    def get_feedback_url(self, safa_refe):
        query = urlencode(
            {
                "banco": self.request.banco,
                "salvo_ref": safa_refe,
            }
        )
        return f"{reverse('tabelasalafami:salafami_criar')}?{query}"
