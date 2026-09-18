from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView
from sindicatospatronais.mixin import SindPatronalMixin
from sindicatospatronais.models import SindicatosPatronais
from sindicatospatronais.services.logic import SindicatoPatronalService, _digits_only
from sindicatospatronais.web.forms import SindicatosPatronaisForm


def _has_errors(form):
    result = {}
    if form is None:
        return result
    for field in form.visible_fields():
        if field.errors:
            result["geral"] = True
    for err in form.non_field_errors():
        result["geral"] = True
    for field in form.hidden_fields():
        if field.errors:
            result["geral"] = True
    return result


class SindicatoPatronalUpdateView(SindPatronalMixin, UpdateView):
    model = SindicatosPatronais
    form_class = SindicatosPatronaisForm
    template_name = "sindicatospatronais/form.html"

    def get_object(self, queryset=None):
        banco_limpo = _digits_only(self.request.banco)
        empr = self.kwargs.get("empr")
        fili = self.kwargs.get("fili")
        codi = self.kwargs.get("codi")
        qs = SindicatosPatronais.objects.using(self.request.db_alias).filter(
            registro=banco_limpo,
            sind_empr=empr,
            sind_fili=fili,
            sind_codi=codi,
        )
        obj = qs.first()
        if obj is None:
            raise Http404
        return obj

    def get_initial(self):
        initial = super().get_initial()
        obj = getattr(self, "object", None)
        if obj is not None:
            initial["registro"] = getattr(obj, "registro", None) or self.banco_limpo
            initial["sind_empr"] = getattr(obj, "sind_empr", None) or self.obter_codigo_empresa_contexto()
            initial["sind_fili"] = getattr(obj, "sind_fili", None) or self.obter_codigo_filial_contexto()
            initial["sind_codi"] = getattr(obj, "sind_codi", None)
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Editar Sindicato Patronal"
        ctx["page_title"] = "Editar Sindicato Patronal"
        ctx["modo_edicao"] = True
        ctx["has_errors"] = _has_errors(ctx["form"])
        obj = getattr(self, "object", None)
        if obj is not None:
            ctx["proximo_codigo"] = getattr(obj, "sind_codi", None)
        ctx["empresa_nome"] = self.obter_nome_empresa_contexto(form=ctx["form"])
        ctx["filial_nome"] = self.obter_nome_filial_contexto(form=ctx["form"])
        return ctx

    def form_valid(self, form):
        try:
            sind_empr = self.obter_codigo_empresa_contexto(form=form)
            sind_fili = self.obter_codigo_filial_contexto(form=form)
            SindicatoPatronalService.salvar_form(
                form=form,
                banco=self.request.banco,
                db_alias=self.db_alias,
                sind_empr=sind_empr,
                sind_fili=sind_fili,
                operacao="editar",
            )
            messages.success(self.request, "Sindicato patronal atualizado com sucesso.")
            return redirect(reverse("sindicatospatronais:listar") + f"?banco={self.request.banco}")
        except Exception as exc:
            messages.error(self.request, str(exc))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Corrija os erros abaixo.")
        return super().form_invalid(form)
