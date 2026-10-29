from django import forms

from prepara_situacoes.models import PreparaSituacoes


CHOICES_GRUPO_SITUACAO = [
    ("", "Selecione"),
    ("Salario maternidade empresa", "Salario maternidade empresa"),
]


def _choice_value(value):
    return str(value or "").strip()


def _append_choice_if_missing(choices, value):
    value_norm = _choice_value(value)
    if not value_norm:
        return choices
    if any(_choice_value(cod) == value_norm for cod, _ in choices):
        return choices
    return [*choices, (value_norm, value_norm)]


class PreparaSituacoesForm(forms.ModelForm):
    class Meta:
        model = PreparaSituacoes
        fields = [
            "registro",
            "prep_empr",
            "prep_fili",
            "prep_codi",
            "prep_desc",
            "prep_descricao",
            "prep_situacao_fixa",
            "prep_desc_situacao_folha",
            "prep_calcula_salario_familia",
            "prep_13_integral",
            "prep_reembolso_gps_13",
            "prep_prorroga_periodo_aquisitivo",
            "prep_meses_media_sindicato",
            "prep_desc_tempo_servico",
            "prep_nao_prorroga_ult_prazo_ferias",
            "prep_perde_pa_afast_super_30",
            "prep_ignora_inss_13",
            "prep_ignora_ir_13",
            "prep_ignora_fgts_13",
            "prep_grupo_situacao",
            "prep_usuario_inc",
            "prep_data_inc",
            "prep_usuario_alt",
            "prep_data_alt",
        ]
        widgets = {
            "registro": forms.HiddenInput(),
            "prep_empr": forms.HiddenInput(),
            "prep_fili": forms.HiddenInput(),
            "prep_codi": forms.HiddenInput(),
            "prep_desc": forms.HiddenInput(),
            "prep_usuario_inc": forms.HiddenInput(),
            "prep_data_inc": forms.HiddenInput(),
            "prep_usuario_alt": forms.HiddenInput(),
            "prep_data_alt": forms.HiddenInput(),
            "prep_descricao": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "maxlength": 250,
                    "placeholder": "Ex.: Prorrogacao Maternidade/Lei 15.156/2025/Zika",
                }
            ),
            "prep_situacao_fixa": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_desc_situacao_folha": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_calcula_salario_familia": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_13_integral": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_reembolso_gps_13": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_prorroga_periodo_aquisitivo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_meses_media_sindicato": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_desc_tempo_servico": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_nao_prorroga_ult_prazo_ferias": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_perde_pa_afast_super_30": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_ignora_inss_13": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_ignora_ir_13": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_ignora_fgts_13": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_grupo_situacao": forms.Select(
                choices=CHOICES_GRUPO_SITUACAO,
                attrs={"class": "form-select form-select-sm"},
            ),
        }
        labels = {
            "prep_descricao": "Descrição",
            "prep_situacao_fixa": "Situacao fixa",
            "prep_desc_situacao_folha": "Descontar situacao na folha",
            "prep_calcula_salario_familia": "Calcula salario familia",
            "prep_13_integral": "13o integral",
            "prep_reembolso_gps_13": "Reembolsa GPS 13o",
            "prep_prorroga_periodo_aquisitivo": "Prorroga periodo aquisitivo",
            "prep_meses_media_sindicato": "Meses de media do sindicato",
            "prep_desc_tempo_servico": "Descontar do tempo de servico",
            "prep_nao_prorroga_ult_prazo_ferias": "Nao prorroga o ultimo prazo de ferias em caso de afastamento",
            "prep_perde_pa_afast_super_30": "Perde PA para afastamento superior 30 dias consecutivos",
            "prep_ignora_inss_13": "INSS 13o",
            "prep_ignora_ir_13": "IR 13o",
            "prep_ignora_fgts_13": "FGTS 13o",
            "prep_grupo_situacao": "Grupo situacao",
        }

    def __init__(self, *args, **kwargs):
        self.db_alias = kwargs.pop("db_alias", None)
        self.banco = kwargs.pop("banco", None)
        self.empr_fixo = kwargs.pop("empr_fixo", 1)
        self.fili_fixo = kwargs.pop("fili_fixo", 1)
        super().__init__(*args, **kwargs)

        for name in (
            "registro",
            "prep_empr",
            "prep_fili",
            "prep_codi",
            "prep_desc",
            "prep_usuario_inc",
            "prep_data_inc",
            "prep_usuario_alt",
            "prep_data_alt",
        ):
            self.fields[name].required = False

        for name in (
            "prep_situacao_fixa",
            "prep_desc_situacao_folha",
            "prep_calcula_salario_familia",
            "prep_13_integral",
            "prep_reembolso_gps_13",
            "prep_prorroga_periodo_aquisitivo",
            "prep_meses_media_sindicato",
            "prep_desc_tempo_servico",
            "prep_nao_prorroga_ult_prazo_ferias",
            "prep_perde_pa_afast_super_30",
            "prep_ignora_inss_13",
            "prep_ignora_ir_13",
            "prep_ignora_fgts_13",
        ):
            self.fields[name].required = False

        current_grupo = None
        if self.instance is not None:
            current_grupo = getattr(self.instance, "prep_grupo_situacao", None)
        self.fields["prep_grupo_situacao"].choices = _append_choice_if_missing(
            CHOICES_GRUPO_SITUACAO,
            current_grupo,
        )

    def clean(self):
        cleaned = super().clean()
        descricao = str(cleaned.get("prep_descricao") or "").strip()
        if descricao and not str(cleaned.get("prep_desc") or "").strip():
            cleaned["prep_desc"] = descricao
        if not descricao:
            self.add_error("prep_descricao", "Informe a descricao.")
        return cleaned

    def validate_unique(self):
        # A tabela usa chave composta no banco (registro, prep_empr, prep_fili, prep_codi).
        # A model Django nao representa essa PK composta, entao a validacao automatica
        # de unicidade do ModelForm gera falso positivo no create.
        return
