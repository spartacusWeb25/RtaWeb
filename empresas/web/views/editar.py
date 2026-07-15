from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from core.banco import get_banco_from_request
from core.mixin import BancoObrigatorioMixin
from core.utils import get_db_from_slug
from empresas.services.chave import EmpresasChaveService
from empresas.services.editar import EmpresasEditarService
from empresas.web.forms import EmpresasForm


class EmpresasUpdateView(BancoObrigatorioMixin, FormView):
    template_name = "empresas/form.html"
    form_class = EmpresasForm
    modo_edicao = True

    def get_chave_dados(self):
        return {
            "registro": self.request.banco,
            "empr_empr": self.kwargs["empresa"],
            "empr_fili": self.kwargs["filial"],
        }

    def get_object(self):
        return EmpresasChaveService.buscar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=self.get_chave_dados(),
        )

    def dispatch(self, request, *args, **kwargs):
        request.banco = getattr(request, "banco", None) or get_banco_from_request(request)
        if not request.banco:
            messages.error(request, "Banco da licença não informado.")
            return redirect(reverse("empresas:listar"))

        request.db_alias = get_db_from_slug(request.banco)
        self.object = self.get_object()

        if not self.object:
            messages.error(request, "Empresa nao encontrada.")
            return redirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        kwargs["banco"] = self.request.banco
        return kwargs

    def form_valid(self, form):
        dados = form.cleaned_data.copy()
        dados["registro"] = self.request.banco
        dados["_original_registro"] = self.request.banco
        dados["_original_empr_empr"] = self.kwargs["empresa"]
        dados["_original_empr_fili"] = self.kwargs["filial"]

        try:
            EmpresasEditarService.editar(
                banco=self.request.banco,
                db_alias=self.request.db_alias,
                dados=dados,
            )
        except ValueError as erro:
            form.add_error(None, str(erro))
            return self.form_invalid(form)

        messages.success(self.request, "Empresa atualizada com sucesso.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("empresas:listar") + f"?banco={self.request.banco}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modo_edicao"] = True
        context["has_errors"] = context["form"].get_tab_errors()
        return context
