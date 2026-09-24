from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from departamentosrh.mixin import DepartamentoRhMixin
from departamentosrh.web.forms import DepartamentoRhForm
from departamentosrh.services.logic import DepartamentosRhService, proximo_codigo_departamento


class DepartamentoRhCreateView(DepartamentoRhMixin, SuccessMessageMixin, CreateView):
    model = None
    form_class = DepartamentoRhForm
    template_name = "departamentosrh/form.html"
    success_message = "Departamento cadastrado com sucesso."

    def get_form(self, form_class=None):
        return super().get_form(form_class=form_class)

    def get_initial(self):
        initial = super().get_initial()
        empr = self.obter_codigo_empresa_contexto()
        fili = self.obter_codigo_filial_contexto()
        try:
            proximo = proximo_codigo_departamento(
                banco=self.banco_limpo, db_alias=self.db_alias, empresa=empr, filial=fili
            )
        except Exception:
            proximo = 1
        initial["registro"] = self.banco_limpo
        initial["depa_empr"] = empr
        initial["depa_fili"] = fili
        initial["depa_codi"] = proximo
        initial["depa_desc"] = None
        initial["depa_inativo"] = False
        initial["depa_tipo_doc"] = 1
        initial["depa_dados_cad_codi"] = 1
        initial["depa_dados_perc_codi"] = 1
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = ctx.get("form")
        empr = self.obter_codigo_empresa_contexto(form=form)
        fili = self.obter_codigo_filial_contexto(form=form)
        try:
            ctx["proximo_codigo"] = proximo_codigo_departamento(
                banco=self.banco_limpo, db_alias=self.db_alias, empresa=empr, filial=fili
            )
        except Exception:
            ctx["proximo_codigo"] = 1
        ctx["operacao"] = "criar"
        ctx["titulo"] = "Novo Departamento"
        ctx["modo_edicao"] = False
        return ctx

    def form_valid(self, form):
        empr = self.obter_codigo_empresa_contexto(form=form)
        fili = self.obter_codigo_filial_contexto(form=form)
        usuario = getattr(self.request, "user", None)
        try:
            DepartamentosRhService.salvar_form(
                form,
                banco=self.banco_limpo,
                db_alias=self.db_alias,
                depa_empr=empr,
                depa_fili=fili,
                operacao="criar",
                usuario=usuario,
            )
        except Exception as exc:
            from django.core.exceptions import ValidationError
            if isinstance(exc, ValidationError):
                try:
                    msg = exc.message % exc.params if exc.params else str(exc)
                except Exception:
                    msg = str(exc)
                form.add_error("depa_codi", msg)
            else:
                form.add_error(None, str(exc))
            return self.form_invalid(form)
        from django.shortcuts import redirect
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("departamentosrh:listar") + f"?banco={self.request.banco or 'rta0001'}"
