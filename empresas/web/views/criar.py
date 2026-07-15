from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from core.banco import get_banco_from_request
from core.mixin import BancoObrigatorioMixin
from core.utils import get_db_from_slug
from empresas.services.criar import EmpresasCriarService
from empresas.web.forms import EmpresasForm


class EmpresasCreateView(BancoObrigatorioMixin, FormView):
    template_name = "empresas/form.html"
    form_class = EmpresasForm

    def dispatch(self, request, *args, **kwargs):
        request.banco = getattr(request, "banco", None) or get_banco_from_request(request)
        if not request.banco:
            messages.error(request, "Banco da licença não informado.")
            return redirect(reverse("empresas:listar"))

        request.db_alias = get_db_from_slug(request.banco)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["banco"] = self.request.banco
        return kwargs

    def form_valid(self, form):
        dados = form.cleaned_data.copy()
        dados["registro"] = self.request.banco

        try:
            EmpresasCriarService.criar(
                banco=self.request.banco,
                db_alias=self.request.db_alias,
                dados=dados,
            )
        except ValueError as erro:
            form.add_error(None, str(erro))
            return self.form_invalid(form)

        messages.success(self.request, "Empresa criada com sucesso.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("empresas:listar") + f"?banco={self.request.banco}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modo_edicao"] = False
        context["has_errors"] = context["form"].get_tab_errors()
        return context
