from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView
from django.utils.safestring import mark_safe
import json
from core.mixin import BancoObrigatorioMixin
from dependentesterc.web.forms import DependentestercForm
from dependentesterc.services.chave import DependentestercChaveService
from dependentesterc.services.editar import DependentestercEditarService
from terceiros.web.choices import CIDADES_POR_CODIGO
from dependentesterc.web.views.criar import (
    _obter_contexto_terceiro,
    _carregar_choices_empresas,
    _carregar_choices_terceiros,
    _digits_only,
)


class DependentestercUpdateView(BancoObrigatorioMixin, FormView):
    template_name = "dependentesterc/form.html"
    form_class = DependentestercForm
    modo_edicao = True

    def get_chave_dados(self):
        return {
            "depe_empr": self.kwargs["empr"],
            "depe_fili": self.kwargs["fili"],
            "depe_terc": self.kwargs["terc"],
            "depe_codi": self.kwargs["codi"],
        }

    def get_object(self):
        banco_limpo = _digits_only(self.request.banco)
        return DependentestercChaveService.buscar(
            banco=banco_limpo,
            db_alias=self.request.db_alias,
            dados=self.get_chave_dados(),
        )

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object:
            messages.error(request, "Dependente de terceiro não encontrado.")
            return redirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        banco_limpo = _digits_only(self.request.banco)

        (
            _,
            empr_padrao_cod,
            _,
            terceiros_por_empfili,
        ) = _carregar_choices_empresas(self.request.db_alias, banco_limpo)
        self._terceiros_por_empfili_json = terceiros_por_empfili
        self._empr_padrao_cod = empr_padrao_cod

        # -- PK composta (hidden): garantir valores corretos do kwargs (URL) --
        form.initial["depe_empr"] = self.kwargs["empr"]
        form.initial["depe_fili"] = self.kwargs["fili"]
        form.initial["depe_terc"] = self.kwargs["terc"]
        form.initial["depe_codi"] = self.kwargs["codi"]
        form.initial["registro"] = banco_limpo

        return form

    def form_valid(self, form):
        banco_limpo = _digits_only(self.request.banco)
        dados = form.cleaned_data.copy()
        dados["registro"]   = banco_limpo              # REGRA RH: SEMPRE pega da licenca/request.banco (limpo)
        dados["depe_empr"]  = int(self.kwargs["empr"]) # REGRA RH: kwargs URL NAO confia em form hidden
        dados["depe_fili"]  = int(self.kwargs["fili"])
        dados["depe_terc"]  = int(self.kwargs["terc"])
        dados["depe_codi"]  = int(self.kwargs["codi"])

        DependentestercEditarService.editar(
            banco=banco_limpo,
            db_alias=self.request.db_alias,
            dados=dados,
        )

        messages.success(self.request, "Dependente de terceiro atualizado com sucesso.")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print("=" * 70)
        print("[DEBUG DepTerc ATUALIZAR form_invalid] form.errors =")
        for k, v in (form.errors or {}).items():
            print(f"  - Campo '{k}': {v}")
        print("[DEBUG DepTerc ATUALIZAR form_invalid] cleaned_data (se existir):")
        try:
            for k, v in (form.cleaned_data or {}).items():
                print(f"  - {k} = {repr(v)[:80]}")
        except Exception:
            pass
        print("=" * 70)
        return super().form_invalid(form)

    def _base_sucesso_url(self):
        banco_limpo = _digits_only(self.request.banco)
        empr = self.kwargs["empr"]
        fili = self.kwargs["fili"]
        terc = self.kwargs["terc"]
        if terc and empr and fili:
            try:
                return (
                    reverse(
                        "terceiros:atualizar",
                        kwargs={
                            "empr": int(empr),
                            "fili": int(fili),
                            "codi": int(terc),
                        },
                    )
                    + f"?banco={banco_limpo}#tab-dependentes"
                )
            except Exception:
                pass
        return reverse("terceiros:listar") + f"?banco={banco_limpo}"

    def get_success_url(self):
        return self._base_sucesso_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banco_limpo = _digits_only(self.request.banco)
        import json
        if not hasattr(self, "_terceiros_por_empfili_json") or not hasattr(self, "_empr_padrao_cod"):
            (
                _,
                empr_padrao_cod,
                _,
                terceiros_json,
            ) = _carregar_choices_empresas(self.request.db_alias, banco_limpo)
        else:
            terceiros_json = self._terceiros_por_empfili_json
            empr_padrao_cod = self._empr_padrao_cod
        context["terceiros_por_empfili_json"] = json.dumps(terceiros_json)
        context["empr_padrao_cod"] = empr_padrao_cod
        context["modo_edicao"] = True
        context["mostrar_cabecalho"] = True
        context["banco_limpo"] = banco_limpo
        # --- FormView NAO injeta object automaticamente (so UpdateView) ---
        context["object"] = self.object
        # --- Modo edição: exibimos o CÓDIGO EXISTENTE do dependente (PK) ---
        context["proximo_codigo_dep"] = self.kwargs["codi"]
        context["terceiro_contexto"] = _obter_contexto_terceiro(
            self.request,
            self.kwargs["empr"],
            self.kwargs["fili"],
            self.kwargs["terc"],
        )
        context["url_voltar"] = self._base_sucesso_url()
        context["cidades_por_codigo_json"] = mark_safe(
            json.dumps(CIDADES_POR_CODIGO, ensure_ascii=False)
        )

        return context
