from django import forms

from funcionarios.models import Funcionarios


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionarios
        fields = [
            "func_empr",
            "func_fili",
            "func_codi",
            "func_nome",
            "func_cpf",
            "func_emai",
            "func_celu",
            "func_seto",
            "func_carg",
        ]
        widgets = {
            "func_empr": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Empresa"}),
            "func_fili": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Filial"}),
            "func_codi": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Código"}),
            "func_nome": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome"}),
            "func_cpf": forms.TextInput(attrs={"class": "form-control", "placeholder": "CPF"}),
            "func_emai": forms.EmailInput(attrs={"class": "form-control", "placeholder": "E-mail"}),
            "func_celu": forms.TextInput(attrs={"class": "form-control", "placeholder": "Celular"}),
            "func_seto": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Setor"}),
            "func_carg": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Cargo"}),
        }
