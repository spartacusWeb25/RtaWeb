from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
import datetime

from aumento_salarial.mixin import AumentoSalarialMixin
from aumento_salarial.services.logic import (
    AumentoSalarialService,
    proximo_codigo_aumento_salarial,
)
from aumento_salarial.web.forms import AumentoSalarialForm


class AumentoSalarialCreateView(AumentoSalarialMixin, SuccessMessageMixin, CreateView):
    model = None
    form_class = AumentoSalarialForm
    template_name = "aumento_salarial/form.html"
    success_message = "Aumento salarial cadastrado com sucesso."

    def get_initial(self):
        initial = super().get_initial()
        empr = self.obter_codigo_empresa_contexto()
        fili = self.obter_codigo_filial_contexto()
        try:
            proximo = proximo_codigo_aumento_salarial(
                banco=self.banco_limpo, db_alias=self.db_alias, empresa=empr, filial=fili
            )
        except Exception:
            proximo = 1
        initial["registro"] = self.banco_limpo
        initial["aume_empr"] = empr
        initial["aume_fili"] = fili
        initial["aume_codi"] = proximo
        initial["aume_tipo_funcionario"] = "T"
        initial["aume_data_alteracao"] = datetime.date.today()
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = ctx.get("form")
        empr = self.obter_codigo_empresa_contexto(form=form)
        fili = self.obter_codigo_filial_contexto(form=form)
        try:
            ctx["proximo_codigo"] = proximo_codigo_aumento_salarial(
                banco=self.banco_limpo, db_alias=self.db_alias, empresa=empr, filial=fili
            )
        except Exception:
            ctx["proximo_codigo"] = 1
        ctx["operacao"] = "criar"
        ctx["titulo"] = "Novo aumento salarial"
        ctx["modo_edicao"] = False
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
                form.add_error("aume_codi", msg)
            else:
                form.add_error(None, str(exc))
            return self.form_invalid(form)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("aumento_salarial:listar") + f"?banco={self.request.banco or 'rta0001'}"
