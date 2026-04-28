from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import CreateView
from funcionarios.services import FuncionariosService
from ...mixin import FuncionarioMixin
from ...utils import _has_errors


class FuncionarioCreateView(FuncionarioMixin, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Novo Funcionário"
        ctx["has_errors"] = _has_errors(ctx["form"])
        return ctx

    def form_valid(self, form):
        try:
            FuncionariosService.salvar_form(db_alias=self.db_alias, form=form)
            messages.success(self.request, "Funcionário cadastrado com sucesso.")
            return redirect(self.request.get_full_path())
        except Exception as exc:
            messages.error(self.request, str(exc))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Corrija os erros abaixo.")
        return super().form_invalid(form)