from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView
from admissaopreliminar.services import AdmissaoPreliminarService
from funcionarios.services import FuncionariosService
from ...mixin import FuncionarioMixin
from ...utils import _has_errors


class FuncionarioCreateView(FuncionarioMixin, CreateView):
    def get_initial(self):
        initial = super().get_initial()
        if not initial.get("func_empr"):
            initial["func_empr"] = self.obter_codigo_empresa_contexto()
        if not initial.get("func_fili"):
            initial["func_fili"] = self.obter_filial_empresa_contexto()

        prefill = self.request.session.get(AdmissaoPreliminarService.SESSION_KEY, {})
        if prefill:
            initial.update(prefill)
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Novo Funcionário"
        ctx["modo_edicao"] = False
        ctx["has_errors"] = _has_errors(ctx["form"])
        ctx["empresa_nome"] = self.obter_nome_empresa_contexto(form=ctx["form"])
        ctx["integracao_esocial_ok"] = False
        ctx["origem_admissao_preliminar"] = bool(
            self.request.session.get(AdmissaoPreliminarService.SESSION_KEY)
        )
        return ctx

    def form_valid(self, form):
        try:
            FuncionariosService.salvar_form(
                banco=self.request.banco,
                db_alias=self.db_alias,
                form=form,
            )
            AdmissaoPreliminarService.consumir_prefill_da_sessao(session=self.request.session)
            messages.success(self.request, "Funcionário cadastrado com sucesso.")
            return redirect(reverse("funcionarios:listar") + f"?banco={self.request.banco}")
        except Exception as exc:
            messages.error(self.request, str(exc))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Corrija os erros abaixo.")
        return super().form_invalid(form)
