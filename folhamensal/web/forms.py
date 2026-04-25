from django import forms

from folhamensal.models import Folhamensal


class FolhaMensalForm(forms.ModelForm):
    class Meta:
        model = Folhamensal
        fields = [
            "fome_empr",
            "fome_fili",
            "fome_func",
            "fome_refe",
            "fome_even",
            "fome_base",
            "fome_perc",
            "fome_valo",
            "fome_tipo",
            "fome_depa",
            "fome_seto",
        ]
        labels = {
            "fome_empr": "Empresa",
            "fome_fili": "Filial",
            "fome_func": "Funcionário",
            "fome_refe": "Referência",
            "fome_even": "Evento",
            "fome_base": "Base",
            "fome_perc": "Percentual",
            "fome_valo": "Valor",
            "fome_tipo": "Tipo",
            "fome_depa": "Departamento",
            "fome_seto": "Setor",
        }
        widgets = {
            "fome_empr": forms.NumberInput(attrs={"class": "form-control"}),
            "fome_fili": forms.NumberInput(attrs={"class": "form-control"}),
            "fome_func": forms.NumberInput(attrs={"class": "form-control"}),
            "fome_refe": forms.TextInput(attrs={"class": "form-control", "placeholder": "YYYYMM", "maxlength": "6"}),
            "fome_even": forms.NumberInput(attrs={"class": "form-control"}),
            "fome_base": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "fome_perc": forms.NumberInput(attrs={"class": "form-control", "step": "0.0001"}),
            "fome_valo": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "fome_tipo": forms.TextInput(attrs={"class": "form-control", "maxlength": "1"}),
            "fome_depa": forms.NumberInput(attrs={"class": "form-control"}),
            "fome_seto": forms.NumberInput(attrs={"class": "form-control"}),
        }
