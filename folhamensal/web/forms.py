from django import forms
from folhamensal.services.chave import FolhaMensalChaveService
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

    def __init__(self, *args, banco=None, db_alias=None, original_chave=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.banco = banco
        self.db_alias = db_alias or "default"
        self.original_chave = original_chave

    def clean(self):
        cleaned = super().clean()

        nova_chave = {
            "registro": self.banco,
            "fome_empr": cleaned.get("fome_empr"),
            "fome_fili": cleaned.get("fome_fili"),
            "fome_func": cleaned.get("fome_func"),
            "fome_refe": cleaned.get("fome_refe"),
            "fome_even": cleaned.get("fome_even"),
        }

        if not all(nova_chave.values()):
            return cleaned

        # edição mantendo a mesma chave: permitido
        if self.original_chave and nova_chave == self.original_chave:
            return cleaned

        existe = FolhaMensalChaveService.existe(
            banco=self.banco,
            db_alias=self.db_alias,
            dados=nova_chave,
        )

        if existe:
            raise forms.ValidationError(
                "Já existe um lançamento para esta empresa, filial, funcionário, referência e evento."
            )

        return cleaned