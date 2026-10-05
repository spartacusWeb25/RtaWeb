from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from prepara_recisoes.mixin import PreparaRescisoesMixin
from prepara_recisoes.web.forms import PreparaRescisoesForm
from prepara_recisoes.services.logic import PreparaRescisoesService, proximo_codigo_prepara_rescisao


class PreparaRescisoesCreateView(PreparaRescisoesMixin, SuccessMessageMixin, CreateView):
    model = None
    form_class = PreparaRescisoesForm
    template_name = "prepara_rescisoes/form.html"
    success_message = "Preparação de rescisão cadastrada com sucesso."

    def get_form(self, form_class=None):
        return super().get_form(form_class=form_class)

    def get_initial(self):
        initial = super().get_initial()
        empr = self.obter_codigo_empresa_contexto()
        fili = self.obter_codigo_filial_contexto()
        try:
            proximo = proximo_codigo_prepara_rescisao(
                banco=self.banco_limpo, db_alias=self.db_alias, empresa=empr, filial=fili
            )
        except Exception:
            proximo = 1
        initial["registro"] = self.banco_limpo
        initial["prep_empr"] = empr
        initial["prep_fili"] = fili
        initial["prep_codi"] = proximo
        initial["prep_inativo"] = False
        # Aviso prévio default = S/Data (codi 4)
        initial["prep_aviso_previo_codi"] = 4
        initial["prep_aviso_previo_desc"] = "S/Data"
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = ctx.get("form")
        empr = self.obter_codigo_empresa_contexto(form=form)
        fili = self.obter_codigo_filial_contexto(form=form)
        try:
            ctx["proximo_codigo"] = proximo_codigo_prepara_rescisao(
                banco=self.banco_limpo, db_alias=self.db_alias, empresa=empr, filial=fili
            )
        except Exception:
            ctx["proximo_codigo"] = 1
        ctx["operacao"] = "criar"
        ctx["titulo"] = "Nova Preparação de Rescisão"
        ctx["modo_edicao"] = False
        return ctx

    def form_valid(self, form):
        empr = self.obter_codigo_empresa_contexto(form=form)
        fili = self.obter_codigo_filial_contexto(form=form)
        usuario = getattr(self.request, "user", None)
        try:
            PreparaRescisoesService.salvar_form(
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
        from django.shortcuts import redirect
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("prepara_recisoes:listar") + f"?banco={self.request.banco or 'rta0001'}"
