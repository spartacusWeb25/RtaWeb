from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView
from core.mixin import BancoObrigatorioMixin
from dependentescontr.web.forms import DependentescontrForm
from dependentescontr.services.chave import DependentescontrChaveService
from dependentescontr.services.editar import DependentescontrEditarService
from dependentescontr.choices import _TOP_CIDADES_IBGE
from dependentescontr.web.views.criar import (
    _obter_contexto_contribuinte,
    _carregar_choices_empresas,
    _carregar_choices_contribuintes,
    _digits_only,
)


class DependentescontrUpdateView(BancoObrigatorioMixin, FormView):
    template_name = "dependentescontr/form.html"
    form_class = DependentescontrForm
    modo_edicao = True

    def get_chave_dados(self):
        return {
            "depecontr_empr": self.kwargs["empr"],
            "depecontr_fili": self.kwargs["fili"],
            "depecontr_contr": self.kwargs["contr"],
            "depecontr_codi": self.kwargs["codi"],
        }

    def get_object(self):
        banco_limpo = _digits_only(self.request.banco)
        return DependentescontrChaveService.buscar(
            banco=banco_limpo,
            db_alias=self.request.db_alias,
            dados=self.get_chave_dados(),
        )

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object:
            messages.error(request, "Dependente de contribuinte não encontrado.")
            return redirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        empr = self.kwargs["empr"]
        fili = self.kwargs["fili"]
        contr = self.kwargs["contr"]
        banco_limpo = _digits_only(self.request.banco)

        (
            choices_empresa_combo,
            empr_padrao_cod,
            _,
            contribuintes_por_empfili,
        ) = _carregar_choices_empresas(self.request.db_alias, banco_limpo)
        self._contribuintes_por_empfili_json = contribuintes_por_empfili
        self._empr_padrao_cod = empr_padrao_cod

        form.fields["depecontr_empr"].choices = choices_empresa_combo
        form.initial["depecontr_empr"] = fili

        form.fields["depecontr_contr"].choices = _carregar_choices_contribuintes(
            contribuintes_por_empfili, empr, fili
        )

        form.fields["depecontr_empr"].disabled = True
        form.fields["depecontr_empr"].widget.attrs["class"] = "form-select"
        form.fields["depecontr_fili"].disabled = True
        form.fields["depecontr_fili"].widget.attrs["class"] = "form-control contribuinte-readonly"
        form.fields["depecontr_contr"].disabled = True
        form.fields["depecontr_contr"].widget.attrs["class"] = "form-select"
        form.fields["depecontr_codi"].initial = self.kwargs["codi"]
        form.fields["depecontr_fili"].initial = fili

        return form

    def form_valid(self, form):
        banco_limpo = _digits_only(self.request.banco)
        dados = form.cleaned_data.copy()
        dados["depecontr_empr"] = self.kwargs["empr"]
        dados["depecontr_fili"] = self.kwargs["fili"]
        dados["depecontr_contr"] = self.kwargs["contr"]
        dados["depecontr_codi"] = self.kwargs["codi"]

        DependentescontrEditarService.editar(
            banco=banco_limpo,
            db_alias=self.request.db_alias,
            dados=dados,
        )

        messages.success(self.request, "Dependente de contribuinte atualizado com sucesso.")
        return redirect(self.get_success_url())

    def _base_sucesso_url(self):
        banco_limpo = _digits_only(self.request.banco)
        empr = self.kwargs["empr"]
        fili = self.kwargs["fili"]
        contr = self.kwargs["contr"]
        if contr and empr and fili:
            try:
                return (
                    reverse(
                        "contribuintes:atualizar",
                        kwargs={
                            "empr": int(empr),
                            "fili": int(fili),
                            "codi": int(contr),
                        },
                    )
                    + f"?banco={banco_limpo}#tab-dependentes"
                )
            except Exception:
                pass
        return reverse("contribuintes:listar") + f"?banco={banco_limpo}"

    def get_success_url(self):
        return self._base_sucesso_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banco_limpo = _digits_only(self.request.banco)
        import json
        if not hasattr(self, "_contribuintes_por_empfili_json") or not hasattr(self, "_empr_padrao_cod"):
            (
                _,
                empr_padrao_cod,
                _,
                contribuintes_json,
            ) = _carregar_choices_empresas(self.request.db_alias, banco_limpo)
        else:
            contribuintes_json = self._contribuintes_por_empfili_json
            empr_padrao_cod = self._empr_padrao_cod
        context["contribuintes_por_empfili_json"] = json.dumps(contribuintes_json)
        context["empr_padrao_cod"] = empr_padrao_cod
        context["modo_edicao"] = True
        context["mostrar_cabecalho"] = True
        context["contribuinte_contexto"] = _obter_contexto_contribuinte(
            self.request,
            self.kwargs["empr"],
            self.kwargs["fili"],
            self.kwargs["contr"],
        )
        context["url_voltar"] = self._base_sucesso_url()

        cidades_lista = []
        for codigo, nome, uf in _TOP_CIDADES_IBGE:
            try:
                codigo_num = int(codigo)
            except Exception:
                continue
            cidades_lista.append(
                {
                    "codigo_str": f"{codigo:0>7}",
                    "codigo_num": codigo_num,
                    "nome": nome,
                    "uf": uf,
                    "label": f"{codigo:0>7} — {nome} / {uf}",
                }
            )
        context["cidades_lista"] = cidades_lista

        return context
