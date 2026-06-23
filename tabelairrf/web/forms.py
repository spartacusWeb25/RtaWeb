from django import forms

from core.utils import format_month_reference, normalize_month_reference
from tabelairrf.models import Tabelairrf


class DecimalCommaField(forms.DecimalField):
    def to_python(self, value):
        if isinstance(value, str):
            value = value.strip()
            if "," in value:
                value = value.replace(".", "").replace(",", ".")
        return super().to_python(value)


class ReferenciaMesAnoField(forms.CharField):
    def __init__(self, *args, **kwargs):
        error_messages = kwargs.setdefault("error_messages", {})
        error_messages.setdefault("invalid", "Informe a referencia no formato MM/AAAA.")
        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        return format_month_reference(value)

    def clean(self, value):
        value = super().clean(value)
        if not value:
            return value

        try:
            return normalize_month_reference(value, strict=True)
        except ValueError as exc:
            raise forms.ValidationError(str(exc))


class TabelairrfForm(forms.ModelForm):
    irrf_refe = ReferenciaMesAnoField(
        label="Referência",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "MM/AAAA",
                "inputmode": "numeric",
                "autocomplete": "off",
                "maxlength": "7",
                "data-refe-input": "true",
            }
        ),
    )
    irrf_fa01 = DecimalCommaField(
        label="Faixa 01",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "inputmode": "decimal", "autocomplete": "off", "data-decimal-input": "true"}),
        error_messages={"invalid": "Informe um valor numérico válido para Faixa 01."},
    )
    irrf_pe01 = DecimalCommaField(
        label="Alíquota 01",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "inputmode": "decimal", "autocomplete": "off", "data-decimal-input": "true"}),
        error_messages={"invalid": "Informe um valor numérico válido para Alíquota 01."},
    )
    irrf_de01 = DecimalCommaField(
        label="Dedução 01",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "inputmode": "decimal", "autocomplete": "off", "data-decimal-input": "true"}),
        error_messages={"invalid": "Informe um valor numérico válido para Dedução 01."},
    )
    irrf_fa02 = DecimalCommaField(
        label="Faixa 02",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "inputmode": "decimal", "autocomplete": "off", "data-decimal-input": "true"}),
        error_messages={"invalid": "Informe um valor numérico válido para Faixa 02."},
    )
    irrf_pe02 = DecimalCommaField(
        label="Alíquota 02",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "inputmode": "decimal", "autocomplete": "off", "data-decimal-input": "true"}),
        error_messages={"invalid": "Informe um valor numérico válido para Alíquota 02."},
    )
    irrf_de02 = DecimalCommaField(
        label="Dedução 02",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "inputmode": "decimal", "autocomplete": "off", "data-decimal-input": "true"}),
        error_messages={"invalid": "Informe um valor numérico válido para Dedução 02."},
    )
    irrf_fa03 = DecimalCommaField(
        label="Faixa 03",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "inputmode": "decimal", "autocomplete": "off", "data-decimal-input": "true"}),
        error_messages={"invalid": "Informe um valor numérico válido para Faixa 03."},
    )
    irrf_pe03 = DecimalCommaField(
        label="Alíquota 03",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "inputmode": "decimal", "autocomplete": "off", "data-decimal-input": "true"}),
        error_messages={"invalid": "Informe um valor numérico válido para Alíquota 03."},
    )
    irrf_de03 = DecimalCommaField(
        label="Dedução 03",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "inputmode": "decimal", "autocomplete": "off", "data-decimal-input": "true"}),
        error_messages={"invalid": "Informe um valor numérico válido para Dedução 03."},
    )
    irrf_fa04 = DecimalCommaField(
        label="Faixa 04",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "inputmode": "decimal", "autocomplete": "off", "data-decimal-input": "true"}),
        error_messages={"invalid": "Informe um valor numérico válido para Faixa 04."},
    )
    irrf_pe04 = DecimalCommaField(
        label="Alíquota 04",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "inputmode": "decimal", "autocomplete": "off", "data-decimal-input": "true"}),
        error_messages={"invalid": "Informe um valor numérico válido para Alíquota 04."},
    )
    irrf_de04 = DecimalCommaField(
        label="Dedução 04",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "inputmode": "decimal", "autocomplete": "off", "data-decimal-input": "true"}),
        error_messages={"invalid": "Informe um valor numérico válido para Dedução 04."},
    )
    irrf_dede = DecimalCommaField(
        label="Valor por Dependente",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "inputmode": "decimal", "autocomplete": "off", "data-decimal-input": "true"}),
        error_messages={"invalid": "Informe um valor numérico válido para Valor por Dependente."},
    )
    irrf_desc_mini = DecimalCommaField(
        label="Desconto Mínimo",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={"invalid": "Informe um valor numérico válido para Desconto Mínimo."},
    )
    irrf_desc_simp = DecimalCommaField(
        label="Desconto Simplificado",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={"invalid": "Informe um valor numérico válido para Desconto Simplificado."},
    )

    def clean_irrf_refe(self):
        irrf_refe = self.cleaned_data.get("irrf_refe")
        if not irrf_refe:
            return irrf_refe

        qs = Tabelairrf.objects.filter(irrf_refe=irrf_refe)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                f"Já existe uma tabela de IRRF para a referência {format_month_reference(irrf_refe)}."
            )

        return irrf_refe

    class Meta:
        model = Tabelairrf
        fields = (
            "irrf_refe",
            "irrf_fa01",
            "irrf_pe01",
            "irrf_de01",
            "irrf_fa02",
            "irrf_pe02",
            "irrf_de02",
            "irrf_fa03",
            "irrf_pe03",
            "irrf_de03",
            "irrf_fa04",
            "irrf_pe04",
            "irrf_de04",
            "irrf_dede",
            "irrf_desc_mini",
            "irrf_desc_simp",
        )
        labels = {
            "irrf_refe": "Referência",
            "irrf_fa01": "Faixa 01",
            "irrf_pe01": "Alíquota 01",
            "irrf_de01": "Dedução 01",
            "irrf_fa02": "Faixa 02",
            "irrf_pe02": "Alíquota 02",
            "irrf_de02": "Dedução 02",
            "irrf_fa03": "Faixa 03",
            "irrf_pe03": "Alíquota 03",
            "irrf_de03": "Dedução 03",
            "irrf_fa04": "Faixa 04",
            "irrf_pe04": "Alíquota 04",
            "irrf_de04": "Dedução 04",
            "irrf_dede": "Valor por Dependente",
            "irrf_desc_mini": "Desconto Mínimo",
            "irrf_desc_simp": "Desconto Simplificado",
        }
        error_messages = {
            "irrf_refe": {
                "required": "Informe a referência.",
            },
        }
