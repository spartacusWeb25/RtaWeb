from django import forms
from core.utils import format_month_reference, normalize_month_reference
from tabelasalafami.models import Tabelasalafami


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


class TabelasalafamiForm(forms.ModelForm):
    safa_refe = ReferenciaMesAnoField(
        label='Referência',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/AAAA'}),
    )
    safa_fa01 = DecimalCommaField(
        label='Salário Família',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': 'Informe um valor numérico válido para Salário Família.'},
    )
    safa_co01 = DecimalCommaField(
        label='Valor',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': 'Informe um valor numérico válido para Valor.'},
    )

    class Meta:
        model = Tabelasalafami
        fields = ('safa_refe', 'safa_fa01', 'safa_co01')
        labels = {
            'safa_refe': 'Referência',
            'safa_fa01': 'Salário Família',
            'safa_co01': 'Valor',
        }
        error_messages = {
            'safa_refe': {
                'required': 'Informe a referência.',
                'unique': 'Já existe uma tabela de salário família com esta referência.',
            },
        }
