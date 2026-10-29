from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from aumento_salarial.mixin import AumentoSalarialMixin
from aumento_salarial.services.logic import AumentoSalarialService
from aumento_salarial.web.forms import AumentoSalarialForm


class AumentoSalarialUpdateView(AumentoSalarialMixin, SuccessMessageMixin, UpdateView):
    model = None
    form_class = AumentoSalarialForm
    template_name = "aumento_salarial/form.html"
    success_message = "Aumento salarial atualizado com sucesso."

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        obj = getattr(self, "object", None)
        if obj is not None and form is not None:
            for fname in ("registro", "aume_empr", "aume_fili", "aume_codi"):
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
            for fname in ("registro", "aume_empr", "aume_fili", "aume_codi"):
                val = getattr(obj, fname, None)
                if val not in (None, "") and fname not in initial:
                    initial[fname] = val
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["operacao"] = "editar"
        ctx["titulo"] = "Editar aumento salarial"
        ctx["modo_edicao"] = True
        obj = getattr(self, "object", None)
        if obj is not None:
            try:
                ctx["proximo_codigo"] = int(getattr(obj, "aume_codi") or 0)
            except Exception:
                ctx["proximo_codigo"] = 0
        return ctx

    def form_valid(self, form):
        empr = self.obter_codigo_empresa_contexto(form=form)
        fili = self.obter_codigo_filial_contexto(form=form)
        usuario = getattr(self.request, "user", None)
        try:
            AumentoSalarialService.salvar_form(
                form,
                banco=self.banco_limpo,
                db_alias=self.db_alias,
                aume_empr=empr,
                aume_fili=fili,
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
                form.add_error("aume_codi", msg)
            else:
                form.add_error(None, str(exc))
            return self.form_invalid(form)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("aumento_salarial:listar") + f"?banco={self.request.banco or 'rta0001'}"
