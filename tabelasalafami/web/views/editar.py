from urllib.parse import urlencode

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView
from core.mixin import BancoObrigatorioMixin
from tabelasalafami.web.forms import TabelasalafamiForm
from tabelasalafami.services.chave import TabelaSalaFamiChaveService
from tabelasalafami.services.editar import SalaFamiEditarService




class TabelasalafamiUpdateView(BancoObrigatorioMixin, FormView):
    template_name = "tabelasalafami/editar.html"  
    form_class = TabelasalafamiForm
    modo_edicao = True

    def get_chave_dados(self):
        return {
            "safa_refe": self.kwargs["safa_refe"],
        }

    def get_object(self):
        return TabelaSalaFamiChaveService.buscar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=self.get_chave_dados(),
        )

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object:
            messages.error(request, "Salário familia não encontrado.")
            return redirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs

    def form_valid(self, form):
        dados = form.cleaned_data.copy()

        dados["safa_refe"] = self.kwargs["safa_refe"]

        SalaFamiEditarService.editar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=dados,
        )

        return redirect(self.get_feedback_url(self.kwargs["safa_refe"]))

    def get_success_url(self):
        return reverse("tabelasalafami:salafami_listar") + f"?banco={self.request.banco}"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modo_edicao"] = True
        safa_refe_editada = self.request.GET.get("editado_ref", "").strip()
        context["mensagem_sucesso_form"] = ""
        context["redirect_delay_ms"] = 1800
        context["redirect_url"] = self.get_success_url()

        if safa_refe_editada:
            context["mensagem_sucesso_form"] = (
                f"Referência {safa_refe_editada} atualizada com sucesso."
            )

        return context

    def get_feedback_url(self, safa_refe):
        query = urlencode(
            {
                "banco": self.request.banco,
                "editado_ref": safa_refe,
            }
        )
        return f"{reverse('tabelasalafami:salafami_editar', kwargs={'safa_refe': safa_refe})}?{query}"
