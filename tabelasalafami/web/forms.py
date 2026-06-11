from django import forms
from tabelasalafami.models import Tabelasalafami


class TabelasalafamiForm(forms.ModelForm): 
    class Meta:
        model = Tabelasalafami     
        fields = ('safa_refe', 'safa_fa01', 'safa_fa02', 'safa_co02')
        widgets = {
            'safa_refe': forms.TextInput(attrs={'class': 'form-control'}),
            'safa_fa01': forms.TextInput(attrs={'class': 'form-control'}),
            'safa_fa02': forms.TextInput(attrs={'class': 'form-control'}),
            'safa_co02': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'safa_refe': 'Referência',
            'safa_fa01': 'Faixa 01',
            'safa_fa02': 'Faixa 02',
            'safa_co02': 'Cota',
        }