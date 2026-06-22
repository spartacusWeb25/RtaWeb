from urllib.parse import urlencode

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from core.mixin import BancoObrigatorioMixin
from core.utils import format_month_reference
from tabelairrf.services.chave import TabelaIrrfChaveService
from tabelairrf.services.editar import TabelaIrrfEditarService
from tabelairrf.web.forms import TabelairrfForm


class TabelairrfUpdateView(BancoObrigatorioMixin, FormView):
    template_name = "tabelairrf/editar.html"
    form_class = TabelairrfForm
    modo_edicao = True

    def get_chave_dados(self):
        return {
            "irrf_refe": self.kwargs["irrf_refe"],
        }

    def get_object(self):
        return TabelaIrrfChaveService.buscar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=self.get_chave_dados(),
        )

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object:
            messages.error(request, "Tabela IRRF não encontrada.")
            return redirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs

    def form_valid(self, form):
        dados = form.cleaned_data.copy()
        dados["irrf_refe"] = self.kwargs["irrf_refe"]

        TabelaIrrfEditarService.editar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=dados,
        )

        return redirect(self.get_feedback_url(self.kwargs["irrf_refe"]))

    def get_success_url(self):
        return reverse("tabelairrf:listar") + f"?banco={self.request.banco}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modo_edicao"] = True
        irrf_refe_editada = self.request.GET.get("editado_ref", "").strip()
        context["mensagem_sucesso_form"] = ""
        context["redirect_delay_ms"] = 1800
        context["redirect_url"] = self.get_success_url()

        if irrf_refe_editada:
            context["mensagem_sucesso_form"] = (
                f"Referência {format_month_reference(irrf_refe_editada)} alterada com sucesso."
            )

        return context

    def get_feedback_url(self, irrf_refe):
        query = urlencode(
            {
                "banco": self.request.banco,
                "editado_ref": irrf_refe,
            }
        )
        return f"{reverse('tabelairrf:irrf_editar', kwargs={'irrf_refe': irrf_refe})}?{query}"
