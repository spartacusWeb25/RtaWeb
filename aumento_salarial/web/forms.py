from django import forms

from aumento_salarial.models import AumentoSalarial
from aumento_salarial.services.logic import (
    AumentoSalarialService,
    FORMA_CHOICES,
    TIPO_FUNCIONARIO_RADIO_CHOICES,
    listar_funcionarios_choices,
)


def _choice_with_current(choices, value):
    value_norm = str(value or "").strip()
    if not value_norm:
        return list(choices)
    if any(str(codigo or "").strip() == value_norm for codigo, _ in choices):
        return list(choices)
    return [*choices, (value_norm, value_norm)]


class AumentoSalarialForm(forms.ModelForm):
    class Meta:
        model = AumentoSalarial
        fields = [
            "registro",
            "aume_empr",
            "aume_fili",
            "aume_codi",
            "aume_func",
            "aume_desc",
            "aume_data_alteracao",
            "aume_data_efeito",
            "aume_motivo",
            "aume_forma",
            "aume_valor",
            "aume_contribuintes",
            "aume_tipo_funcionario",
            "aume_classe",
            "aume_cargo",
            "aume_departamento",
            "aume_centro_custo",
            "aume_sindicato",
            "aume_salario_atual",
            "aume_aumento_proporcional",
            "aume_arredondar_salario",
            "aume_alterar_meses_posteriores",
            "aume_demitidos_mes",
            "aume_admitidos_mes",
            "aume_usuario_inc",
            "aume_data_inc",
            "aume_usuario_alt",
            "aume_data_alt",
            "log_data",
            "log_hora",
        ]
        widgets = {
            "registro": forms.HiddenInput(),
            "aume_empr": forms.HiddenInput(),
            "aume_fili": forms.HiddenInput(),
            "aume_codi": forms.HiddenInput(),
            "aume_usuario_inc": forms.HiddenInput(),
            "aume_data_inc": forms.HiddenInput(),
            "aume_usuario_alt": forms.HiddenInput(),
            "aume_data_alt": forms.HiddenInput(),
            "log_data": forms.HiddenInput(),
            "log_hora": forms.HiddenInput(),
            "aume_func": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "aume_desc": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "maxlength": 200,
                    "placeholder": "Descrição do aumento salarial",
                }
            ),
            "aume_data_alteracao": forms.DateInput(
                attrs={"class": "form-control form-control-sm", "type": "date"},
                format="%Y-%m-%d",
            ),
            "aume_data_efeito": forms.DateInput(
                attrs={"class": "form-control form-control-sm", "type": "date"},
                format="%Y-%m-%d",
            ),
            "aume_motivo": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "maxlength": 200,
                    "placeholder": "Motivo do aumento salarial",
                }
            ),
            "aume_forma": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "aume_valor": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "aume_contribuintes": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "aume_tipo_funcionario": forms.RadioSelect(
                attrs={"class": "form-check-input"},
                choices=TIPO_FUNCIONARIO_RADIO_CHOICES,
            ),
            "aume_classe": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "aume_cargo": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "aume_departamento": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "aume_centro_custo": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "aume_sindicato": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "aume_salario_atual": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "aume_aumento_proporcional": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "aume_arredondar_salario": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "aume_alterar_meses_posteriores": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "aume_demitidos_mes": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "aume_admitidos_mes": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "aume_func": "Funcionário",
            "aume_desc": "Descrição do aumento",
            "aume_data_alteracao": "Data da alteração",
            "aume_data_efeito": "Data de efeito",
            "aume_motivo": "Motivo",
            "aume_forma": "Forma",
            "aume_valor": "Valor",
            "aume_contribuintes": "Contribuintes",
            "aume_tipo_funcionario": "Tipo de funcionário",
            "aume_classe": "Classe",
            "aume_cargo": "Cargo",
            "aume_departamento": "Departamento",
            "aume_centro_custo": "Centro de custo",
            "aume_sindicato": "Sindicato",
            "aume_salario_atual": "Salário atual",
            "aume_aumento_proporcional": "Aumento de salário proporcional para admitidos no último ano",
            "aume_arredondar_salario": "Arredondar salário",
            "aume_alterar_meses_posteriores": "Alterar meses posteriores",
            "aume_demitidos_mes": "Demitidos no mês",
            "aume_admitidos_mes": "Admitidos no mês",
        }

    def __init__(self, *args, **kwargs):
        self.db_alias = kwargs.pop("db_alias", None)
        self.banco = kwargs.pop("banco", None)
        self.empr_fixo = kwargs.pop("empr_fixo", 1)
        self.fili_fixo = kwargs.pop("fili_fixo", 1)
        super().__init__(*args, **kwargs)

        for name in (
            "registro",
            "aume_empr",
            "aume_fili",
            "aume_codi",
            "aume_usuario_inc",
            "aume_data_inc",
            "aume_usuario_alt",
            "aume_data_alt",
            "log_data",
            "log_hora",
        ):
            self.fields[name].required = False

        for name in (
            "aume_contribuintes",
            "aume_aumento_proporcional",
            "aume_arredondar_salario",
            "aume_alterar_meses_posteriores",
            "aume_demitidos_mes",
            "aume_admitidos_mes",
        ):
            self.fields[name].required = False

        self.fields["aume_func"].required = False
        self.fields["aume_data_alteracao"].input_formats = ["%Y-%m-%d"]
        self.fields["aume_data_efeito"].input_formats = ["%Y-%m-%d"]
        self.fields["aume_tipo_funcionario"].required = False

        if self.instance is not None:
            self.fields["aume_data_alteracao"].initial = getattr(self.instance, "aume_data_alteracao", None)
            self.fields["aume_data_efeito"].initial = getattr(self.instance, "aume_data_efeito", None)

        valor_func = self._current_value("aume_func")
        self.fields["aume_func"].choices = listar_funcionarios_choices(
            banco=self.banco,
            db_alias=self.db_alias,
            codigo_empresa=self.empr_fixo,
            codigo_filial=self.fili_fixo,
            valor_atual=valor_func,
        )
        self.fields["aume_func"].widget.choices = self.fields["aume_func"].choices

        valor_forma = self._current_value("aume_forma")
        self.fields["aume_forma"].choices = _choice_with_current(FORMA_CHOICES, valor_forma)
        self.fields["aume_forma"].widget.choices = self.fields["aume_forma"].choices

        valor_tipo = self._current_value("aume_tipo_funcionario")
        self.fields["aume_tipo_funcionario"].choices = _choice_with_current(TIPO_FUNCIONARIO_RADIO_CHOICES, valor_tipo)

        self._set_select_choices("aume_classe", AumentoSalarialService.choices_classes(db_alias=self.db_alias, valor_atual=self._current_value("aume_classe")))
        self._set_select_choices(
            "aume_cargo",
            AumentoSalarialService.choices_cargos(
                banco=self.banco,
                db_alias=self.db_alias,
                codigo_empresa=self.empr_fixo,
                codigo_filial=self.fili_fixo,
                valor_atual=self._current_value("aume_cargo"),
            ),
        )
        self._set_select_choices(
            "aume_departamento",
            AumentoSalarialService.choices_departamentos(
                banco=self.banco,
                db_alias=self.db_alias,
                codigo_empresa=self.empr_fixo,
                codigo_filial=self.fili_fixo,
                valor_atual=self._current_value("aume_departamento"),
            ),
        )
        self._set_select_choices(
            "aume_centro_custo",
            AumentoSalarialService.choices_centro_custo(
                banco=self.banco,
                db_alias=self.db_alias,
                codigo_empresa=self.empr_fixo,
                valor_atual=self._current_value("aume_centro_custo"),
            ),
        )
        self._set_select_choices(
            "aume_sindicato",
            AumentoSalarialService.choices_sindicatos(
                banco=self.banco,
                db_alias=self.db_alias,
                codigo_empresa=self.empr_fixo,
                codigo_filial=self.fili_fixo,
                valor_atual=self._current_value("aume_sindicato"),
            ),
        )

    def _current_value(self, field_name):
        if self.is_bound:
            return self.data.get(field_name)
        if self.instance is not None:
            return getattr(self.instance, field_name, None)
        return self.initial.get(field_name)

    def _set_select_choices(self, field_name, choices):
        self.fields[field_name].choices = choices
        self.fields[field_name].widget.choices = choices

    def clean(self):
        cleaned = super().clean()
        descricao = str(cleaned.get("aume_desc") or "").strip()
        if not descricao:
            self.add_error("aume_desc", "Informe a descrição do aumento.")
        if not str(cleaned.get("aume_forma") or "").strip():
            self.add_error("aume_forma", "Selecione a forma.")
        if cleaned.get("aume_valor") in (None, ""):
            self.add_error("aume_valor", "Informe o valor do aumento.")
        if not cleaned.get("aume_data_alteracao"):
            self.add_error("aume_data_alteracao", "Informe a data da alteração.")
        return cleaned

    def validate_unique(self):
        return
