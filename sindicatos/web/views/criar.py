from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from sindicatos.mixin import SindicatoTrabalhadoresMixin
from sindicatos.services.logic import SindicatoTrabalhadoresService, proximo_codigo_sindicato, _digits_only
from sindicatos.web.forms import SindicatosTrabalhadoresForm


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


class SindicatoTrabalhadoresCreateView(SindicatoTrabalhadoresMixin, CreateView):
    model = SindicatosTrabalhadoresForm.Meta.model
    form_class = SindicatosTrabalhadoresForm
    template_name = "sindicatos/form.html"
    success_url = reverse_lazy("sindicatos:listar")

    def get_initial(self):
        initial = super().get_initial()
        empr = self.obter_codigo_empresa_contexto()
        fili = self.obter_codigo_filial_contexto()
        if not initial.get("sind_empr"):
            initial["sind_empr"] = empr
        if not initial.get("sind_fili"):
            initial["sind_fili"] = fili
        if (
            (not initial.get("sind_codi") or not str(initial.get("sind_codi") or "").isdigit())
            and getattr(self.request, "banco", None)
            and empr
            and fili
        ):
            try:
                initial["sind_codi"] = proximo_codigo_sindicato(
                    banco=_digits_only(self.request.banco),
                    db_alias=self.db_alias,
                    empresa=int(empr),
                    filial=int(fili),
                )
            except Exception:
                initial["sind_codi"] = 1
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Novo Sindicato Trabalhador"
        ctx["page_title"] = "Novo Sindicato Trabalhador"
        ctx["modo_edicao"] = False
        ctx["has_errors"] = _has_errors(ctx["form"])
        ctx["proximo_codigo"] = self.get_initial().get("sind_codi")
        ctx["empresa_nome"] = self.obter_nome_empresa_contexto(form=ctx["form"])
        ctx["filial_nome"] = self.obter_nome_filial_contexto(form=ctx["form"])
        return ctx

    def form_valid(self, form):
        try:
            sind_empr = self.obter_codigo_empresa_contexto(form=form)
            sind_fili = self.obter_codigo_filial_contexto(form=form)
            SindicatoTrabalhadoresService.salvar_form(
                form=form,
                banco=self.request.banco,
                db_alias=self.db_alias,
                sind_empr=sind_empr,
                sind_fili=sind_fili,
                operacao="criar",
            )
            messages.success(self.request, "Sindicato trabalhador cadastrado com sucesso.")
            return redirect(reverse("sindicatos:listar") + f"?banco={self.request.banco}")
        except ValidationError as exc:
            form.add_error("sind_codi", "Ja existe um sindicato trabalhador com este codigo e filial nesta licenca.")
            return self.form_invalid(form)
        except Exception as exc:
            messages.error(self.request, str(exc))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Corrija os erros abaixo.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("sindicatos:listar") + f"?banco={self.request.banco}"
