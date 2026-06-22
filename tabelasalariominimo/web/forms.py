from django import forms
from core.utils import format_month_reference, normalize_month_reference
from tabelasalariominimo.models import Tabelasalariominimo


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


class TabelasalariominimoForm(forms.ModelForm):
    refe_sala_mini = ReferenciaMesAnoField(
        label='Referência',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/AAAA'}),
    )
    refe_sala_mini_fede = DecimalCommaField(
        label='Salário Mínimo',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': 'Informe um valor numérico válido para Salário Mínimo.'},
    )

    class Meta:
        model = Tabelasalariominimo
        fields = ('refe_sala_mini', 'refe_sala_mini_fede')
        labels = {
            'refe_sala_mini': 'Referência',
            'refe_sala_mini_fede': 'Salário Mínimo',
        }
        error_messages = {
            'refe_sala_mini': {
                'required': 'Informe a referência.',
                'unique': 'Já existe uma tabela de salário mínimo com esta referência.',
            },
        }
