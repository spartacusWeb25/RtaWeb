from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView
from funcionarios.services import FuncionariosService
from funcionarios.mixin import FuncionarioMixin
from funcionarios.utils import _has_errors


class FuncionarioUpdateView(FuncionarioMixin, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Editar Funcionário"
        ctx["modo_edicao"] = True
        ctx["has_errors"] = _has_errors(ctx["form"])
        ctx["empresa_nome"] = self.obter_nome_empresa_contexto(form=ctx["form"])
        ctx["integracao_esocial_ok"] = bool(getattr(self.object, "func_integracao_esocial", False))

        try:
            from dependentesrh.models import Dependentesrh

            if self.object and self.request.banco and self.request.db_alias:
                empr = getattr(self.object, "func_empr", None)
                fili = getattr(self.object, "func_fili", None)
                codi = getattr(self.object, "func_codi", None)
                if empr is not None and fili is not None and codi is not None:
                    deps = list(
                        Dependentesrh.objects.using(self.request.db_alias)
                        .filter(
                            registro=self.request.banco,
                            depe_empr=int(empr),
                            depe_fili=int(fili),
                            depe_func=int(codi),
                        )
                        .order_by("depe_codi")
                        .all()
                    )
                    ctx["dependentes_funcionario"] = deps
                    ctx["dependentes_qtd"] = len(deps)
                    ctx["dependentes_url_criar"] = (
                        reverse("dependentesrh:criar")
                        + f"?banco={self.request.banco}&empresa={int(empr)}&filial={int(fili)}&funcionario={int(codi)}"
                    )
        except Exception:
            ctx["dependentes_funcionario"] = []
            ctx["dependentes_qtd"] = 0
            ctx["dependentes_url_criar"] = ""

        return ctx

    def form_valid(self, form):
        try:
            FuncionariosService.salvar_form(
                banco=self.request.banco,
                db_alias=self.request.db_alias,
                form=form,
            )
            messages.success(self.request, "Funcionário atualizado com sucesso.")
            return redirect(reverse("funcionarios:listar") + f"?banco={self.request.banco}")
        except Exception as exc:
            messages.error(self.request, str(exc))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Corrija os erros abaixo.")
        return super().form_invalid(form)
