from django import forms
from tabelasalafami.models import Tabelasalafami


class DecimalCommaField(forms.DecimalField):
    def to_python(self, value):
        if isinstance(value, str):
            value = value.strip()
            if "," in value:
                value = value.replace(".", "").replace(",", ".")
        return super().to_python(value)


class TabelasalafamiForm(forms.ModelForm):
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
        widgets = {
            'safa_refe': forms.TextInput(attrs={'class': 'form-control'}),
        }
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
