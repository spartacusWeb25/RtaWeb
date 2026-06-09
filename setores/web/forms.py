from django import forms
from setores.models import Setoresrh


class SetoresrhForm(forms.ModelForm):
    class Meta:
        model = Setoresrh
        fields = ('registro', 'seto_empr', 'seto_codi', 'seto_desc', 'seto_sigl', 'seto_cecu', 'seto_obse')
        widgets = {
            'registro': forms.TextInput(attrs={'class': 'form-control'}),
            'seto_empr': forms.TextInput(attrs={'class': 'form-control'}),
            'seto_codi': forms.TextInput(attrs={'class': 'form-control'}),
            'seto_desc': forms.TextInput(attrs={'class': 'form-control'}),
            'seto_sigl': forms.TextInput(attrs={'class': 'form-control'}),
            'seto_cecu': forms.TextInput(attrs={'class': 'form-control'}),
            'seto_obse': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'registro': 'Registro',
            'seto_empr': 'Empresa',
            'seto_codi': 'Código',
            'seto_desc': 'Descrição',
            'seto_sigl': 'Sigla',
            'seto_cecu': 'Cecu',
            'seto_obse': 'Observação',
        }