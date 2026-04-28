from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import UpdateView
from funcionarios.services import FuncionariosService
from funcionarios.mixin import FuncionarioMixin
from funcionarios.utils import _has_errors


class FuncionarioUpdateView(FuncionarioMixin, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = f"Editar — {self.object.func_nome or self.object.func_codi}"
        ctx["has_errors"] = _has_errors(ctx["form"])
        return ctx

    def form_valid(self, form):
        try:
            FuncionariosService.salvar_form(banco=self.request.banco, form=form)
            messages.success(self.request, "Funcionário atualizado com sucesso.")
            return redirect(self.request.get_full_path())
        except Exception as exc:
            messages.error(self.request, str(exc))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Corrija os erros abaixo.")
        return super().form_invalid(form)