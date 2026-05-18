from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView
from core.mixin import BancoObrigatorioMixin
from setores.web.forms import SetoresrhForm
from setores.services.chave import SetoresChaveService
from setores.services.editar import SetoresEditarService




class SetoresrhUpdateView(BancoObrigatorioMixin, FormView):
    template_name = "setores/criar.html"
    form_class = SetoresrhForm
    modo_edicao = True

    def get_chave_dados(self):
        return {
            "seto_empr": self.kwargs["empresa"],
            "seto_codi": self.kwargs["codigo"],
        }

    def get_object(self):
        return SetoresChaveService.buscar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=self.get_chave_dados(),
        )

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object:
            messages.error(request, "Setor não encontrado.")
            return redirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs

    def form_valid(self, form):
        dados = form.cleaned_data.copy()

        dados["seto_empr"] = self.kwargs["empresa"]
        dados["seto_codi"] = self.kwargs["codigo"]

        SetoresEditarService.editar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=dados,
        )

        messages.success(self.request, "Setor atualizado com sucesso.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("setores:setoresrh_listar") + f"?banco={self.request.banco}"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modo_edicao"] = True
        return context