from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from cargos.mixin import CargosMixin
from cargos.web.forms import CargosForm
from cargos.models import Cargos
from cargos.services.logic import CargosService, _digits_only


class CargoUpdateView(CargosMixin, SuccessMessageMixin, UpdateView):
    model = Cargos
    form_class = CargosForm
    template_name = "cargos/form.html"
    success_message = "Cargo atualizado com sucesso."

    def get_object(self, queryset=None):
        empr = int(self.kwargs.get("empr") or 0)
        fili = int(self.kwargs.get("fili") or 0)
        codi = int(self.kwargs.get("codi") or 0)
        banco_limpo = _digits_only(self.request.banco or "")
        qs = Cargos.objects.using(self.db_alias).filter(
            registro=banco_limpo,
            carg_empr=empr,
            carg_fili=fili,
            carg_codi=codi,
        )
        return get_object_or_404(qs)

    def get_initial(self):
        initial = super().get_initial()
        obj = getattr(self, "object", None)
        banco_limpo = _digits_only(self.request.banco or "")
        initial["registro"] = banco_limpo
        if obj is not None:
            initial["carg_empr"] = getattr(obj, "carg_empr", None)
            initial["carg_fili"] = getattr(obj, "carg_fili", None)
            initial["carg_codi"] = getattr(obj, "carg_codi", None)
            initial["carg_descricao"] = getattr(obj, "carg_descricao", None)
            initial["carg_inativo"] = getattr(obj, "carg_inativo", False)
            initial["carg_cbo_codi"] = getattr(obj, "carg_cbo_codi", None)
            initial["carg_cbo_desc"] = getattr(obj, "carg_cbo_desc", None)
        else:
            initial["carg_empr"] = None
            initial["carg_fili"] = None
            initial["carg_codi"] = None
            initial["carg_descricao"] = None
            initial["carg_inativo"] = False
            initial["carg_cbo_codi"] = None
            initial["carg_cbo_desc"] = None
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obj = getattr(self, "object", None)
        if obj is not None:
            ctx["proximo_codigo"] = getattr(obj, "carg_codi", None)
        ctx["operacao"] = "editar"
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
                operacao="editar",
            )
        except Exception as exc:
            from django.core.exceptions import ValidationError
            if isinstance(exc, ValidationError):
                form.add_error(
                    "carg_codi",
                    exc.message % exc.params if exc.params else str(exc)
                )
            else:
                form.add_error(None, str(exc))
            return self.form_invalid(form)
        from django.shortcuts import redirect
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("cargos:listar") + f"?banco={self.request.banco or 'rta0001'}"
