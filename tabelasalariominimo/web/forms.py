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
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'MM/AAAA',
                'inputmode': 'numeric',
                'autocomplete': 'off',
                'maxlength': '7',
                'data-refe-input': 'true',
            }
        ),
    )
    refe_sala_mini_fede = DecimalCommaField(
        label='Salário Mínimo',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'inputmode': 'decimal',
                'autocomplete': 'off',
                'data-decimal-input': 'true',
            }
        ),
        error_messages={'invalid': 'Informe um valor numérico válido para Salário Mínimo.'},
    )

    def clean_refe_sala_mini(self):
        refe_sala_mini = self.cleaned_data.get("refe_sala_mini")
        if not refe_sala_mini:
            return refe_sala_mini

        qs = Tabelasalariominimo.objects.filter(refe_sala_mini=refe_sala_mini)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                f"Já existe uma tabela de salário mínimo para a referência {format_month_reference(refe_sala_mini)}."
            )

        return refe_sala_mini

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
            },
        }
