from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from cargos.mixin import CargosMixin
from cargos.web.forms import CargosForm
from cargos.services.logic import CargosService, proximo_codigo_cargo


class CargoCreateView(CargosMixin, SuccessMessageMixin, CreateView):
    model = None
    form_class = CargosForm
    template_name = "cargos/form.html"
    success_message = "Cargo cadastrado com sucesso."

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    def get_initial(self):
        initial = super().get_initial()
        empr = self.obter_codigo_empresa_contexto()
        fili = self.obter_codigo_filial_contexto()
        try:
            proximo = proximo_codigo_cargo(
                banco=self.banco_limpo, db_alias=self.db_alias, empresa=empr, filial=fili
            )
        except Exception:
            proximo = 1
        initial["registro"] = self.banco_limpo
        initial["carg_empr"] = empr
        initial["carg_fili"] = fili
        initial["carg_codi"] = proximo
        initial["carg_descricao"] = None
        initial["carg_inativo"] = False
        initial["carg_cbo_codi"] = None
        initial["carg_cbo_desc"] = None
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = ctx.get("form")
        empr = self.obter_codigo_empresa_contexto(form=form)
        fili = self.obter_codigo_filial_contexto(form=form)
        try:
            ctx["proximo_codigo"] = proximo_codigo_cargo(
                banco=self.banco_limpo, db_alias=self.db_alias, empresa=empr, filial=fili
            )
        except Exception:
            ctx["proximo_codigo"] = 1
        ctx["operacao"] = "criar"
        return ctx

    def form_valid(self, form):
        empr = self.obter_codigo_empresa_contexto(form=form)
        fili = self.obter_codigo_filial_contexto(form=form)
        try:
            CargosService.salvar_form(
                form,
                banco=self.banco_limpo,
                db_alias=self.db_alias,
                carg_empr=empr,
                carg_fili=fili,
                operacao="criar",
            )
        except Exception as exc:
            from django.core.exceptions import ValidationError
            if isinstance(exc, ValidationError):
                form.add_error("carg_codi", exc.message % exc.params if exc.params else str(exc))
            else:
                form.add_error(None, str(exc))
            return self.form_invalid(form)
        from django.shortcuts import redirect
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("cargos:listar") + f"?banco={self.request.banco or 'rta0001'}"
