from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView
from core.mixin import BancoObrigatorioMixin
from dependentesrh.web.forms import DependentesrhForm
from dependentesrh.services.chave import DependentesChaveService
from dependentesrh.services.editar import DependentesEditarService
from dependentesrh.web.choices import _TOP_CIDADES_IBGE
from dependentesrh.web.views.criar import (
    _obter_contexto_funcionario,
    _carregar_choices_empresas,
    _carregar_choices_funcionarios,
)


class DependentesrhUpdateView(BancoObrigatorioMixin, FormView):
    template_name = "dependentesrh/form.html"
    form_class = DependentesrhForm
    modo_edicao = True

    def get_chave_dados(self):
        return {
            "depe_empr": self.kwargs["empresa"],
            "depe_fili": self.kwargs["filial"],
            "depe_func": self.kwargs["funcionario"],
            "depe_codi": self.kwargs["codigo"],
        }

    def get_object(self):
        return DependentesChaveService.buscar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=self.get_chave_dados(),
        )

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object:
            messages.error(request, "Dependente não encontrado.")
            return redirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        empr = self.kwargs["empresa"]
        fili = self.kwargs["filial"]
        func = self.kwargs["funcionario"]

        (
            choices_empresa_combo,
            empr_padrao_cod,
            _,
            funcionarios_por_empfili,
        ) = _carregar_choices_empresas(self.request.db_alias, self.request.banco)
        self._funcionarios_por_empfili_json = funcionarios_por_empfili
        self._empr_padrao_cod = empr_padrao_cod

        form.fields["depe_empr"].choices = choices_empresa_combo
        form.initial["depe_empr"] = fili

        form.fields["depe_func"].choices = _carregar_choices_funcionarios(
            funcionarios_por_empfili, empr, fili
        )

        form.fields["depe_empr"].disabled = True
        form.fields["depe_empr"].widget.attrs["class"] = "form-select"
        form.fields["depe_fili"].disabled = True
        form.fields["depe_fili"].widget.attrs["class"] = "form-control funcionario-readonly"
        form.fields["depe_func"].disabled = True
        form.fields["depe_func"].widget.attrs["class"] = "form-select"
        form.fields["depe_codi"].initial = self.kwargs["codigo"]
        form.fields["depe_fili"].initial = fili

        return form

    def form_valid(self, form):
        dados = form.cleaned_data.copy()
        dados["depe_empr"] = self.kwargs["empresa"]
        dados["depe_fili"] = self.kwargs["filial"]
        dados["depe_func"] = self.kwargs["funcionario"]
        dados["depe_codi"] = self.kwargs["codigo"]

        DependentesEditarService.editar(
            banco=self.request.banco,
            db_alias=self.request.db_alias,
            dados=dados,
        )

        messages.success(self.request, "Dependente atualizado com sucesso.")
        return redirect(self.get_success_url())

    def _base_sucesso_url(self):
        empr = self.kwargs["empresa"]
        fili = self.kwargs["filial"]
        func = self.kwargs["funcionario"]
        if func and empr and fili:
            try:
                return (
                    reverse(
                        "funcionarios:atualizar",
                        kwargs={
                            "func_empr": int(empr),
                            "func_fili": int(fili),
                            "func_codi": int(func),
                        },
                    )
                    + f"?banco={self.request.banco}#tab-parentes"
                )
            except Exception:
                pass
        return reverse("dependentesrh:listar") + f"?banco={self.request.banco}"

    def get_success_url(self):
        return self._base_sucesso_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        import json
        if not hasattr(self, "_funcionarios_por_empfili_json") or not hasattr(self, "_empr_padrao_cod"):
            (
                _,
                empr_padrao_cod,
                _,
                funcionarios_json,
            ) = _carregar_choices_empresas(self.request.db_alias, self.request.banco)
        else:
            funcionarios_json = self._funcionarios_por_empfili_json
            empr_padrao_cod = self._empr_padrao_cod
        context["funcionarios_por_empfili_json"] = json.dumps(funcionarios_json)
        context["empr_padrao_cod"] = empr_padrao_cod
        context["modo_edicao"] = True
        context["mostrar_cabecalho"] = True
        context["funcionario_contexto"] = _obter_contexto_funcionario(
            self.request,
            self.kwargs["empresa"],
            self.kwargs["filial"],
            self.kwargs["funcionario"],
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
