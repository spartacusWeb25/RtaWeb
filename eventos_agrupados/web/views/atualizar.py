from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from eventos_agrupados.mixin import EventosAgrupadosMixin
from eventos_agrupados.services.logic import EventosAgrupadosService
from eventos_agrupados.web.forms import EventosAgrupadosForm


class EventosAgrupadosUpdateView(EventosAgrupadosMixin, SuccessMessageMixin, UpdateView):
    model = None
    form_class = EventosAgrupadosForm
    template_name = "eventos_agrupados/form.html"
    success_message = "Configuração de eventos agrupados atualizado com sucesso."

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        obj = getattr(self, "object", None)
        if obj is not None and form is not None:
            for fname in ("registro", "even_empr", "even_fili"):
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
            for fname in ("registro", "even_empr", "even_fili"):
                val = getattr(obj, fname, None)
                if val not in (None, "") and fname not in initial:
                    initial[fname] = val
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["operacao"] = "editar"
        ctx["titulo"] = "Editar evento agrupado para cálculo"
        ctx["modo_edicao"] = True
        return ctx

    def form_valid(self, form):
        empr = self.obter_codigo_empresa_contexto(form=form)
        fili = self.obter_codigo_filial_contexto(form=form)
        try:
            EventosAgrupadosService.salvar_form(
                form,
                banco=self.banco_limpo,
                db_alias=self.db_alias,
                even_empr=empr,
                even_fili=fili,
                operacao="editar",
            )
        except Exception as exc:
            from django.core.exceptions import ValidationError

            if isinstance(exc, ValidationError):
                form.add_error(None, str(exc))
            else:
                form.add_error(None, str(exc))
            return self.form_invalid(form)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("eventos_agrupados:listar") + f"?banco={self.request.banco or 'rta0001'}"
