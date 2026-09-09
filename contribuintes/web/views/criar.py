from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from contribuintes.mixin import ContribuinteMixin
from contribuintes.services.logic import ContribuintesService
from contribuintes.utils import _has_errors


class ContribuinteCreateView(ContribuinteMixin, CreateView):
    success_url = reverse_lazy("contribuintes:listar")

    def get_initial(self):
        initial = super().get_initial()
        if not initial.get("contr_empr"):
            initial["contr_empr"] = self.obter_codigo_empresa_contexto()
        if not initial.get("contr_fili"):
            initial["contr_fili"] = self.obter_codigo_filial_contexto()
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Novo Contribuinte"
        ctx["modo_edicao"] = False
        ctx["has_errors"] = _has_errors(ctx["form"])
        ctx["empresa_nome"] = self.obter_nome_empresa_contexto(form=ctx["form"])
        ctx["filial_nome"] = self.obter_nome_filial_contexto(form=ctx["form"])
        ctx["integracao_esocial_ok"] = False
        ctx["dependentescontr_list"] = []
        ctx["dependentescontr_qtd"] = 0
        ctx["dependentescontr_url_criar"] = ""
        ctx["paises_lista"] = self.obter_paises_lista()
        ctx["cidades_lista"] = self.obter_cidades_lista()
        return ctx

    def form_valid(self, form):
        try:
            contr_empr = self.obter_codigo_empresa_contexto(form=form)
            contr_fili = self.obter_codigo_filial_contexto(form=form)
            ContribuintesService.salvar_form(
                form=form,
                banco=self.request.banco,
                db_alias=self.db_alias,
                contr_empr=contr_empr,
                contr_fili=contr_fili,
            )
            messages.success(self.request, "Contribuinte cadastrado com sucesso.")
            return redirect(reverse("contribuintes:listar") + f"?banco={self.request.banco}")
        except Exception as exc:
            messages.error(self.request, str(exc))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Corrija os erros abaixo.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("contribuintes:listar") + f"?banco={self.request.banco}"
