from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from prepara_situacoes.mixin import PreparaSituacoesMixin
from prepara_situacoes.services.logic import (
    PreparaSituacoesService,
    proximo_codigo_prepara_situacao,
)
from prepara_situacoes.web.forms import PreparaSituacoesForm


class PreparaSituacoesCreateView(PreparaSituacoesMixin, SuccessMessageMixin, CreateView):
    model = None
    form_class = PreparaSituacoesForm
    template_name = "prepara_situacoes/form.html"
    success_message = "Preparação de situação cadastrada com sucesso."

    def get_initial(self):
        initial = super().get_initial()
        empr = self.obter_codigo_empresa_contexto()
        fili = self.obter_codigo_filial_contexto()
        try:
            proximo = proximo_codigo_prepara_situacao(
                banco=self.banco_limpo, db_alias=self.db_alias, empresa=empr, filial=fili
            )
        except Exception:
            proximo = 1
        initial["registro"] = self.banco_limpo
        initial["prep_empr"] = empr
        initial["prep_fili"] = fili
        initial["prep_codi"] = proximo
        initial["prep_situacao_fixa"] = False
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = ctx.get("form")
        empr = self.obter_codigo_empresa_contexto(form=form)
        fili = self.obter_codigo_filial_contexto(form=form)
        try:
            ctx["proximo_codigo"] = proximo_codigo_prepara_situacao(
                banco=self.banco_limpo, db_alias=self.db_alias, empresa=empr, filial=fili
            )
        except Exception:
            ctx["proximo_codigo"] = 1
        ctx["operacao"] = "criar"
        ctx["titulo"] = "Nova Preparação de situação"
        ctx["modo_edicao"] = False
        return ctx

    def form_valid(self, form):
        empr = self.obter_codigo_empresa_contexto(form=form)
        fili = self.obter_codigo_filial_contexto(form=form)
        usuario = getattr(self.request, "user", None)
        try:
            PreparaSituacoesService.salvar_form(
                form,
                banco=self.banco_limpo,
                db_alias=self.db_alias,
                prep_empr=empr,
                prep_fili=fili,
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
                form.add_error("prep_codi", msg)
            else:
                form.add_error(None, str(exc))
            return self.form_invalid(form)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("prepara_situacoes:listar") + f"?banco={self.request.banco or 'rta0001'}"
