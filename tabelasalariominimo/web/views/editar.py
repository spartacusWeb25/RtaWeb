from urllib.parse import urlencode

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView
from core.mixin import BancoObrigatorioMixin
from core.utils import format_month_reference
from tabelasalariominimo.web.forms import TabelasalariominimoForm
from tabelasalariominimo.services.chave import TabelaSalarioMinimoChaveService
from tabelasalariominimo.services.editar import SalarioMinimoEditarService




class TabelasalariominimoUpdateView(BancoObrigatorioMixin, FormView):
    template_name = "tabelasalariominimo/editar.html"  
    form_class = TabelasalariominimoForm
    modo_edicao = True

    def get_chave_dados(self):
        return {
            "refe_sala_mini": self.kwargs["refe_sala_mini"],
        }

    def get_object(self):
        return TabelaSalarioMinimoChaveService.buscar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=self.get_chave_dados(),
        )

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object:
            messages.error(request, "Salário mínimo não encontrado.")
            return redirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs

    def form_valid(self, form):
        dados = form.cleaned_data.copy()
        dados["_original_refe_sala_mini"] = self.kwargs["refe_sala_mini"]

        salariominimo = SalarioMinimoEditarService.editar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=dados,
        )

        return redirect(self.get_feedback_url(salariominimo.refe_sala_mini))

    def get_success_url(self):
        return reverse("tabelasalariominimo:listar") + f"?banco={self.request.banco}"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modo_edicao"] = True
        refe_sala_mini_editada = self.request.GET.get("editado_ref", "").strip()
        context["mensagem_sucesso_form"] = ""
        context["redirect_delay_ms"] = 1800
        context["redirect_url"] = self.get_success_url()

        if refe_sala_mini_editada:
            context["mensagem_sucesso_form"] = (
                f"Referência {format_month_reference(refe_sala_mini_editada)} atualizada com sucesso."
            )

        return context

    def get_feedback_url(self, refe_sala_mini):
        query = urlencode(
            {
                "banco": self.request.banco,
                "editado_ref": refe_sala_mini,
            }
        )
        return f"{reverse('tabelasalariominimo:salariominimo_editar', kwargs={'refe_sala_mini': refe_sala_mini})}?{query}"        
