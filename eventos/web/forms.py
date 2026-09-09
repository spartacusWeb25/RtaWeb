from django import forms
from django.db import models as db_models
from eventos.models import Eventos
from eventos.web.choices import (
    TIPO_REFERENCIA_CHOICES,
    TIPO_VERBA_CHOICES,
    NATUREZA_RUBRICA_CHOICES,
    TETO_REMUNERATORIO_CHOICES,
    INCIDENCIA_CPRP_CHOICES,
    FUNCIONARIOS_AFASTADOS_CHOICES,
)


ESOCIAL_PLACEHOLDER_CHOICES = (("", "Selecione"),)
VERBA_NEGATIVA_ESOCIAL_CHOICES = (("", "Selecione"),)


def _choices_with_current(choices_tuple, current_value):
    if current_value is None or current_value == "":
        return choices_tuple

    valores_atuais = {str(v) for v, _ in choices_tuple}
    atual = str(current_value)
    if atual in valores_atuais:
        return choices_tuple

    extra = [(current_value, f"{current_value} — {current_value}")]
    return (*choices_tuple, extra)


class EventoForm(forms.ModelForm):

    COMBO_CHOICES_FIELDS = (
        ("even_tipo_verba", TIPO_VERBA_CHOICES),
        ("even_natureza_rubrica", NATUREZA_RUBRICA_CHOICES),
        ("even_tipo_referencia", TIPO_REFERENCIA_CHOICES),
        ("even_teto_remuneratorio_cf", TETO_REMUNERATORIO_CHOICES),
        ("even_incidencia_cprp", INCIDENCIA_CPRP_CHOICES),
        ("even_funcionarios_afastados", FUNCIONARIOS_AFASTADOS_CHOICES),
        ("even_esocial_1", ESOCIAL_PLACEHOLDER_CHOICES),
        ("even_esocial_2", ESOCIAL_PLACEHOLDER_CHOICES),
        ("even_esocial_3", ESOCIAL_PLACEHOLDER_CHOICES),
        ("even_esocial_4", ESOCIAL_PLACEHOLDER_CHOICES),
        ("even_verba_negativa_esocial", VERBA_NEGATIVA_ESOCIAL_CHOICES),
    )

    class Meta:
        model = Eventos
        exclude = ("registro", "even_log_data", "even_log_hora")
        labels = {
            "even_empr": "Empresa",
            "even_codi": "Código",
            "even_desc": "Descrição",
            "even_inativo": "Inativo",

            # --- Aba 1 — Incidência
            "even_classificacao": "Classificação",
            "even_natureza_rubrica": "Natureza da rubrica",
            "even_tipo_referencia": "Tipo referência",
            "even_tipo_verba": "Tipo verba",
            "even_incide_inss": "INSS",
            "even_incide_fgts": "FGTS",
            "even_incide_ir": "IRRF",
            "even_incide_pis_pasep": "PIS / PASEP",
            "even_incide_contribuicoes_sindicais": "Contribuições sindicais",
            "even_incide_base_salario_familia": "Base salário família",
            "even_esocial_1": "Código eSocial 1",
            "even_esocial_2": "Código eSocial 2",
            "even_esocial_3": "Código eSocial 3",
            "even_esocial_4": "Código eSocial 4",

            # --- Aba 2 — Características
            "even_flag_horas_extras": "Horas extras",
            "even_percentual_horas_extras": "% Hora extra",
            "even_rendimento_variavel": "Rendimento variável",
            "even_comissao": "Comissão",
            "even_dsr_salario": "DSR sobre salário",
            "even_dsr_horas_extras": "DSR sobre horas extras",
            "even_dsr_rendimentos_variaveis": "DSR sobre rendimentos variáveis",
            "even_indenizacao_rescisao_contrato": "Indenização rescisão contrato",
            "even_ajuda_custo_diarias": "Ajuda custo / diárias",
            "even_grava_ficha_horas_normais": "Gravar ficha horas normais",
            "even_adicional_dirigente_sindical": "Adicional dirigente sindical",
            "even_media_horas_adicional_noturno": "Média horas / adicional noturno",
            "even_plano_saude_empresarial": "Plano saúde empresarial",
            "even_reembolso_despesas_medicas": "Reembolso despesas médicas",
            "even_despesas_judiciarias": "Despesas judiciárias",
            "even_distribuicao_lucros": "Distribuição de lucros",
            "even_previdencia_privada": "Previdência privada",
            "even_fapi": "FAPI",
            "even_pensao_alimenticia": "Pensão alimentícia",
            "even_previdencia_oficial": "Previdência oficial",
            "even_desconto_compulsorio": "Desconto compulsório",
            "even_salario_garantia": "Salário garantia",
            "even_taxa_servico": "Taxa de serviço",
            "even_medias_sobre_valores": "Médias sobre valores",
            "even_somente_tomador_principal": "Somente tomador principal",
            "even_rendimento_isento_irrf": "Rendimento isento IRRF",
            "even_nao_considera_para_estouro": "Não considera p/ estouro",
            "even_descontar_pensao_paga_13": "Descontar pensão no 13º",
            "even_descontar_pensao_paga_adto13": "Descontar pensão ADT 13º",
            "even_imprimir_verba_zerada": "Imprimir verba zerada",
            "even_ferias_folha_credito_trabalha": "Férias folha crédito trab.",
            "even_verba_negativa_esocial": "Verba negativa para o eSocial",
            "even_teto_remuneratorio_cf": "Teto remuneratório (art. 37, XI, da CF/1988)",
            "even_incidencia_cprp": "Incidência CPRP",
            "even_funcionarios_afastados": "Funcionários afastados",
            "even_observacao": "Observação",

            # --- Aba 3 — Fórmulas
            "even_formula_ref1": "Referência 1",
            "even_formula_ref2": "Referência 2",
            "even_formula_ref3": "Referência 3",
            "even_formula_valo1": "Valor / Fórmula 1",
            "even_formula_valo2": "Valor / Fórmula 2",
            "even_formula_valo3": "Valor / Fórmula 3",
        }

    def __init__(self, *args, **kwargs):
        self.db_alias = kwargs.pop("db_alias", None)
        super().__init__(*args, **kwargs)

        for nome, field in self.fields.items():
            model_field = self._meta.model._meta.get_field(nome)

            if isinstance(model_field, db_models.BooleanField):
                valor_atual = (
                    self.initial.get(nome)
                    or (self.instance.pk and getattr(self.instance, nome, None))
                )
                novo = forms.BooleanField(
                    required=False,
                    initial=bool(valor_atual) if valor_atual not in (None, "") else False,
                    widget=forms.CheckboxInput(
                        check_test=lambda v: bool(v) if v not in (None, "") else False,
                        attrs={
                            "class": "form-check-input",
                            "disabled": False,
                        },
                    ),
                )
                novo.label = field.label
                self.fields[nome] = novo
                continue

            if isinstance(model_field, db_models.DateField):
                field.widget = forms.DateInput(
                    attrs={"class": "form-control", "type": "date"},
                    format="%Y-%m-%d",
                )
                field.input_formats = ["%Y-%m-%d"]
                continue

            if isinstance(model_field, db_models.TimeField):
                field.widget = forms.TimeInput(
                    attrs={"class": "form-control", "type": "time"},
                    format="%H:%M",
                )
                continue

            if isinstance(model_field, db_models.TextField):
                field.widget = forms.TextInput(attrs={
                    "class": "form-control",
                    "maxlength": "500",
                })
                continue

            if isinstance(model_field, (db_models.IntegerField, db_models.DecimalField)):
                widget = field.widget
                if not isinstance(widget, forms.NumberInput):
                    widget = forms.NumberInput()
                    field.widget = widget
                widget.attrs["class"] = "form-control"
                if isinstance(model_field, db_models.DecimalField):
                    widget.attrs.setdefault("step", "0.01")
                continue

            field.widget.attrs["class"] = "form-control"

        short_text_fields = (
            "even_esocial_1 even_esocial_2 even_esocial_3 even_esocial_4 "
            "even_classificacao even_natureza_rubrica even_tipo_referencia"
        )
        for nome in short_text_fields.split():
            if nome in self.fields:
                self.fields[nome].widget.attrs.setdefault("maxlength", 20)

        for field_name, choices in self.COMBO_CHOICES_FIELDS:
            if field_name not in self.fields:
                continue
            atual = self.initial.get(field_name) or (
                self.instance.pk and getattr(self.instance, field_name, None)
            )
            self.fields[field_name].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(choices, atual),
            )
            self.fields[field_name].required = False

        if "even_percentual_horas_extras" in self.fields:
            self.fields["even_percentual_horas_extras"].widget.attrs["step"] = "0.0001"

        if "even_observacao" in self.fields:
            self.fields["even_observacao"].widget = forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": "500",
            })

        for nome in ("even_formula_valo1", "even_formula_valo2", "even_formula_valo3"):
            if nome in self.fields:
                widget = self.fields[nome].widget
                if not isinstance(widget, forms.Textarea):
                    widget = forms.Textarea(attrs={"rows": 2})
                    self.fields[nome].widget = widget
                widget.attrs["class"] = "form-control font-monospace"

        if "even_empr" in self.fields:
            self.fields["even_empr"].widget = forms.HiddenInput()
            self.fields["even_empr"].required = False
