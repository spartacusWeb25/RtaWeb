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
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': 'Informe um valor numérico válido para a Faixa 01.'},
    )
    safa_co01 = DecimalCommaField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': 'Informe um valor numérico válido para a Cota 01.'},
    )
    safa_fa02 = DecimalCommaField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': 'Informe um valor numérico válido para a Faixa 02.'},
    )
    safa_co02 = DecimalCommaField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': 'Informe um valor numérico válido para a Cota 02.'},
    )

    class Meta:
        model = Tabelasalafami
        fields = ('safa_refe', 'safa_fa01', 'safa_co01', 'safa_fa02', 'safa_co02')
        widgets = {
            'safa_refe': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'safa_refe': 'Referência',
            'safa_fa01': 'Faixa 01',
            'safa_co01': 'Cota 01',
            'safa_fa02': 'Faixa 02',
            'safa_co02': 'Cota 02',
        }
        error_messages = {
            'safa_refe': {
                'required': 'Informe a referência.',
                'unique': 'Já existe uma tabela de salário família com esta referência.',
            },
        }
