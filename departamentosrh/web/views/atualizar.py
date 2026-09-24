from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from departamentosrh.mixin import DepartamentoRhMixin
from departamentosrh.web.forms import DepartamentoRhForm
from departamentosrh.services.logic import DepartamentosRhService


class DepartamentoRhUpdateView(DepartamentoRhMixin, SuccessMessageMixin, UpdateView):
    model = None
    form_class = DepartamentoRhForm
    template_name = "departamentosrh/form.html"
    success_message = "Departamento atualizado com sucesso."

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        obj = getattr(self, "object", None)
        if obj is not None and form is not None:
            for fname in ("registro", "depa_empr", "depa_fili", "depa_codi"):
                if fname in form.fields:
                    try:
                        form.fields[fname].widget.attrs["value"] = getattr(obj, fname, None) or ""
                    except Exception:
                        pass
                    form.fields[fname].required = False
        return form

    def get_initial(self):
        initial = super().get_initial()
        obj = getattr(self, "object", None)
        if obj is not None:
            for fname in ("registro", "depa_empr", "depa_fili", "depa_codi"):
                val = getattr(obj, fname, None)
                if val not in (None, "") and fname not in initial:
                    initial[fname] = val
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["operacao"] = "editar"
        ctx["titulo"] = "Editar Departamento"
        ctx["modo_edicao"] = True
        obj = getattr(self, "object", None)
        if obj is not None:
            try:
                ctx["proximo_codigo"] = int(getattr(obj, "depa_codi") or 0)
            except Exception:
                ctx["proximo_codigo"] = 0
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
                operacao="editar",
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
