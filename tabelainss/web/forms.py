from django import forms
from core.utils import format_month_reference, normalize_month_reference
from tabelainss.models import Tabelainss


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


class TabelainssForm(forms.ModelForm):
    tabe_refe = ReferenciaMesAnoField(
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
    tabe_fa01 = DecimalCommaField(
        label='Faixa 01',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'decimal', 'autocomplete': 'off', 'data-decimal-input': 'true'}),
        error_messages={'invalid': 'Informe um valor numérico válido para Faixa 01.'},
    )
    tabe_pe01 = DecimalCommaField(
        label='Alíquota 01',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'decimal', 'autocomplete': 'off', 'data-decimal-input': 'true'}),
        error_messages={'invalid': 'Informe um valor numérico válido para Alíquota 01.'},
    )
    tabe_fa02 = DecimalCommaField(
        label='Faixa 02',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'decimal', 'autocomplete': 'off', 'data-decimal-input': 'true'}),
        error_messages={'invalid': 'Informe um valor numérico válido para Faixa 02.'},
    )
    tabe_pe02 = DecimalCommaField(
        label='Alíquota 02',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'decimal', 'autocomplete': 'off', 'data-decimal-input': 'true'}),
        error_messages={'invalid': 'Informe um valor numérico válido para Alíquota 02.'},
    )
    tabe_fa03 = DecimalCommaField(
        label='Faixa 03',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'decimal', 'autocomplete': 'off', 'data-decimal-input': 'true'}),
        error_messages={'invalid': 'Informe um valor numérico válido para Faixa 03.'},
    )
    tabe_pe03 = DecimalCommaField(
        label='Alíquota 03',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'decimal', 'autocomplete': 'off', 'data-decimal-input': 'true'}),
        error_messages={'invalid': 'Informe um valor numérico válido para Alíquota 03.'},
    )
    tabe_fa04 = DecimalCommaField(
        label='Faixa 04',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'decimal', 'autocomplete': 'off', 'data-decimal-input': 'true'}),
        error_messages={'invalid': 'Informe um valor numérico válido para Faixa 04.'},
    )
    tabe_pe04 = DecimalCommaField(
        label='Alíquota 04',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'decimal', 'autocomplete': 'off', 'data-decimal-input': 'true'}),
        error_messages={'invalid': 'Informe um valor numérico válido para Alíquota 04.'},
    )
    tabe_mini_gps = DecimalCommaField(
        label='Valor Mínimo GPS',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'decimal', 'autocomplete': 'off', 'data-decimal-input': 'true'}),
        error_messages={'invalid': 'Informe um valor numérico válido para Valor Mínimo GPS.'},
    )

    def clean_tabe_refe(self):
        tabe_refe = self.cleaned_data.get("tabe_refe")
        if not tabe_refe:
            return tabe_refe

        qs = Tabelainss.objects.filter(tabe_refe=tabe_refe)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                f"Já existe uma tabela de INSS para a referência {format_month_reference(tabe_refe)}."
            )

        return tabe_refe

    class Meta:
        model = Tabelainss
        fields = (
            'tabe_refe',
            'tabe_fa01',
            'tabe_pe01',
            'tabe_fa02',
            'tabe_pe02',
            'tabe_fa03',
            'tabe_pe03',
            'tabe_fa04',
            'tabe_pe04',
            'tabe_mini_gps',
        )
        labels = {
            'tabe_refe': 'Referência',
            'tabe_fa01': 'Faixa 01',
            'tabe_pe01': 'Alíquota 01',
            'tabe_fa02': 'Faixa 02',
            'tabe_pe02': 'Alíquota 02',
            'tabe_fa03': 'Faixa 03',
            'tabe_pe03': 'Alíquota 03',
            'tabe_fa04': 'Faixa 04',
            'tabe_pe04': 'Alíquota 04',
            'tabe_mini_gps': 'Valor Mínimo GPS',
        }
        error_messages = {
            'tabe_refe': {
                'required': 'Informe a referência.',
            },
        }
