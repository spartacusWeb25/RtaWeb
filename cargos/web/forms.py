from datetime import date
from django import forms
from django.core.exceptions import ValidationError

from cargos.models import Cargos
from cargos.services.logic import _digits_only


FIELD_LABELS = {
    "carg_codi": "Código",
    "carg_descricao": "Descrição",
    "carg_inativo": "Inativo",
    "carg_cbo_codi": "CBO",
    "carg_cbo_desc": "",
}

_DIGITS_ONLY_FIELDS = (
    "carg_codi",
    "carg_cbo_codi",
)

_NUMERIC_SAFE_FIELDS = (
    "carg_empr",
    "carg_fili",
    "carg_codi",
    "carg_cbo_codi",
)


def _safe_int(value):
    if value in (None, ""):
        return None
    try:
        v = _digits_only(value)
        if v == "":
            return None
        return int(v)
    except Exception:
        return None


class CargosForm(forms.ModelForm):

    class Meta:
        model = Cargos
        fields = "__all__"
        labels = FIELD_LABELS
        widgets = {
            "registro": forms.HiddenInput(),
            "carg_empr": forms.HiddenInput(),
            "carg_fili": forms.HiddenInput(),
            "carg_codi": forms.HiddenInput(),
            "carg_descricao": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Ex.: Analista de sistemas",
                    "maxlength": 200,
                }
            ),
            "carg_inativo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "carg_cbo_codi": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Cód.",
                    "data-digits-only": "true",
                    "inputmode": "numeric",
                    "maxlength": 7,
                }
            ),
            "carg_cbo_desc": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Descrição CBO",
                    "maxlength": 200,
                }
            ),
        }

    def __init__(self, *args, db_alias=None, banco=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_alias = db_alias or "default"
        self.banco = banco

        for fname in _DIGITS_ONLY_FIELDS:
            if fname in self.fields:
                f = self.fields[fname]
                attrs = dict(f.widget.attrs or {})
                attrs.setdefault("data-digits-only", "true")
                attrs.setdefault("inputmode", "numeric")
                f.widget.attrs = attrs

        for fname, field in self.fields.items():
            if fname.startswith("carg_") and fname != "carg_inativo":
                field.required = False

        if "carg_inativo" in self.fields:
            self.fields["carg_inativo"].required = False

    def clean_carg_codi(self):
        return _safe_int(self.cleaned_data.get("carg_codi"))

    def clean_carg_empr(self):
        return _safe_int(self.cleaned_data.get("carg_empr"))

    def clean_carg_fili(self):
        return _safe_int(self.cleaned_data.get("carg_fili"))

    def clean_carg_cbo_codi(self):
        return _safe_int(self.cleaned_data.get("carg_cbo_codi"))

    def validate_unique(self):
        banco_limpo = _digits_only(self.banco or "")
        empr = _safe_int(self.cleaned_data.get("carg_empr"))
        fili = _safe_int(self.cleaned_data.get("carg_fili"))
        codi = _safe_int(self.cleaned_data.get("carg_codi"))

        if not all([banco_limpo, empr, fili, codi]):
            return

        qs = Cargos.objects.using(self.db_alias).filter(
            registro=banco_limpo,
            carg_empr=int(empr),
            carg_fili=int(fili),
            carg_codi=int(codi),
        )

        instance = getattr(self, "instance", None)
        is_editar = False
        if instance is not None:
            try:
                pk_parts = (
                    getattr(instance, "registro", None),
                    getattr(instance, "carg_empr", None),
                    getattr(instance, "carg_fili", None),
                    getattr(instance, "carg_codi", None),
                )
                is_editar = all(v is not None for v in pk_parts)
            except Exception:
                is_editar = False
        if is_editar:
            qs = qs.exclude(
                registro=getattr(instance, "registro"),
                carg_empr=getattr(instance, "carg_empr"),
                carg_fili=getattr(instance, "carg_fili"),
                carg_codi=getattr(instance, "carg_codi"),
            )

        if qs.exists():
            self.add_error(
                "carg_codi",
                f"Já existe um Cargo cadastrado com o Código {codi} para a Empresa/Filial selecionada."
            )

    def clean(self):
        cd = super().clean() or {}
        today = date.today()
        if self.instance is not None:
            self.instance.field_log_data = today
        return cd
