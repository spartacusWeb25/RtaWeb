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

        messages.success(self.request, "Salário familia atualizado com sucesso.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("tabelasalafami:salafami_listar") + f"?banco={self.request.banco}"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modo_edicao"] = True
        return context
