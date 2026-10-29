from django import forms

from eventos_agrupados.models import EventosAgrupados
from eventos_agrupados.services.logic import EVENTO_FIELDS, listar_eventos_choices


FIELD_LABELS = {
    "even_ferias_proporcionais": "Ferias proporcionais",
    "even_ferias_vencidas": "Ferias vencidas",
    "even_ferias_dobro": "Ferias em dobro",
    "even_ferias_indenizadas": "Ferias indenizadas",
    "even_13_salario": "13º salario",
    "even_13_salario_indenizado": "13º salario indenizado",
    "even_aviso_previo_indenizado": "Aviso previo indenizado",
}


def _safe_int(value):
    try:
        if value is None:
            return None
        text = str(value).strip()
        if not text or not text.isdigit():
            return None
        return int(text)
    except Exception:
        return None


class EventosAgrupadosForm(forms.ModelForm):
    class Meta:
        model = EventosAgrupados
        fields = [
            "registro",
            "even_empr",
            "even_fili",
            "even_ferias_proporcionais",
            "even_ferias_vencidas",
            "even_ferias_dobro",
            "even_ferias_indenizadas",
            "even_13_salario",
            "even_13_salario_indenizado",
            "even_aviso_previo_indenizado",
        ]
        widgets = {
            "registro": forms.HiddenInput(),
            "even_empr": forms.HiddenInput(),
            "even_fili": forms.HiddenInput(),
            "even_ferias_proporcionais": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "even_ferias_vencidas": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "even_ferias_dobro": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "even_ferias_indenizadas": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "even_13_salario": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "even_13_salario_indenizado": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "even_aviso_previo_indenizado": forms.Select(attrs={"class": "form-select form-select-sm"}),
        }
        labels = FIELD_LABELS

    def __init__(self, *args, **kwargs):
        self.db_alias = kwargs.pop("db_alias", None)
        self.banco = kwargs.pop("banco", None)
        self.empr_fixo = kwargs.pop("empr_fixo", 1)
        self.fili_fixo = kwargs.pop("fili_fixo", 1)
        super().__init__(*args, **kwargs)

        for name in ("registro", "even_empr", "even_fili"):
            self.fields[name].required = False

        for field_name in EVENTO_FIELDS:
            self.fields[field_name].required = False
            valor_atual = None
            if self.is_bound:
                valor_atual = self.data.get(field_name)
            elif self.instance is not None:
                valor_atual = getattr(self.instance, field_name, None)
            choices = listar_eventos_choices(
                banco=self.banco,
                db_alias=self.db_alias,
                codigo_empresa=self.empr_fixo,
                valor_atual=valor_atual,
            )
            self.fields[field_name].choices = choices
            self.fields[field_name].widget.choices = choices

    def clean(self):
        cleaned = super().clean()
        for field_name in EVENTO_FIELDS:
            cleaned[field_name] = _safe_int(cleaned.get(field_name))
        return cleaned

    def validate_unique(self):
        # A tabela usa chave composta no banco (registro, even_empr, even_fili).
        # A model Django nao representa essa PK composta, entao a validacao padrao
        # do ModelForm gera falso positivo ao criar.
        return
