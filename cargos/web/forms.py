from datetime import date
from django import forms
from django.core.exceptions import ValidationError

from cargos.models import Cargos
from cargos.services.logic import _digits_only, CargosService


FIELD_LABELS = {
    "carg_codi": "Código",
    "carg_descricao": "Descrição",
    "carg_inativo": "Inativo",
    "carg_cbo_codi": "CBO",
    "carg_cbo_desc": "",
}

_DIGITS_ONLY_FIELDS = (
    "carg_codi",
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

    # Sobrescreve o IntegerField do model para CharField, pois o usuário coloca
    # o texto "724315 - Soldador" no input; depois nós extraímos o cód no clean
    # e convertemos de volta para IntegerField.
    carg_cbo_codi = forms.CharField(
        required=False,
        label="CBO",
        max_length=300,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-sm",
                "placeholder": "Selecione...",
                "maxlength": 300,
                "autocomplete": "off",
                "data-role": "cbo-search",
                "style": "border-top-right-radius:0;border-bottom-right-radius:0;",
            }
        ),
    )

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
            "carg_cbo_desc": forms.HiddenInput(),
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

        # ====== MONTAR MAPA DE CBOs PARA O TEMPLATE (Pesquisa Dinâmica Custom) ======
        # Injetamos um JSON no context atraves do CargosMixin, mas tambem guardamos aqui para o clean()
        # Usamos TODAS as 10.185 linhas (sinonimos inclusos) para pesquisa no frontend.
        self._cbo_lista_completa: list[dict[str, str]] = []   # [{"codi":"724315","desc":"Soldador"}, {"codi":"724315","desc":"Montador soldador"}, ...]
        self._cbo_desc_principal_por_cod: dict[str, str] = {}  # cod -> descricao PRINCIPAL para salvar no banco
        try:
            cbos_lista = CargosService.listar_cbos(banco=self.banco or "", db_alias=self.db_alias)
            cbos_lista_salva: list[dict[str, str]] = []
            for item in cbos_lista:
                cod = str(item.get("codi", "")).strip()
                desc = str(item.get("desc", "")).strip()
                if not cod or not desc:
                    continue
                cbos_lista_salva.append({"codi": cod, "desc": desc})
                if cod not in self._cbo_desc_principal_por_cod:
                    self._cbo_desc_principal_por_cod[cod] = desc
            self._cbo_lista_completa = cbos_lista_salva
        except Exception as exc:
            print(f"[CBO Form] Erro ao carregar lista de CBOs do tab_cbo: {exc}")

        # Garante que carg_cbo_desc é Hidden
        if "carg_cbo_desc" in self.fields:
            self.fields["carg_cbo_desc"].required = False
            self.fields["carg_cbo_desc"].widget = forms.HiddenInput()

        if "carg_cbo_codi" in self.fields:
            self.fields["carg_cbo_codi"].required = False
            self.fields["carg_cbo_codi"].widget.attrs["class"] = "form-control form-control-sm"
            self.fields["carg_cbo_codi"].widget.attrs.setdefault("placeholder", "Selecione...")

    def clean_carg_codi(self):
        return _safe_int(self.cleaned_data.get("carg_codi"))

    def clean_carg_empr(self):
        return _safe_int(self.cleaned_data.get("carg_empr"))

    def clean_carg_fili(self):
        return _safe_int(self.cleaned_data.get("carg_fili"))

    def clean_carg_cbo_codi(self):
        # O input pode receber:
        #   a) "724315 - Soldador" → extrair "724315" (antes do " - ")
        #   b) apenas os dígitos "724315" → manter
        #   c) texto vazio ou "Selecione..." → retornar None
        valor = self.cleaned_data.get("carg_cbo_codi")
        if not valor:
            return None
        if isinstance(valor, int):
            return _safe_int(valor)
        s = str(valor).strip()
        if not s or s.lower().startswith("selecione"):
            return None
        # Caso (a): tem " - " → parte da esquerda é o cód
        if " - " in s:
            s = s.split(" - ", 1)[0].strip()
        return _safe_int(s)

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

        # ===== SALVAR AUTOMATICAMENTE A DESCRICAO CBO PRINCIPAL A PARTIR DO CODIGO =====
        codi_int = cd.get("carg_cbo_codi") if cd else None
        # Caso contrario, tenta buscar do raw POST por via dos campos do form
        if codi_int is None and cd is not None:
            raw_codi = cd.get("carg_cbo_codi")
            if raw_codi not in (None, ""):
                codi_int = _safe_int(raw_codi)

        if codi_int:
            codi_str = str(int(codi_int))
            desc_principal = (self._cbo_desc_principal_por_cod.get(codi_str, None) or "").strip()
            cd["carg_cbo_codi"] = int(codi_int)
            cd["carg_cbo_desc"] = desc_principal
            if self.instance is not None:
                self.instance.carg_cbo_codi = int(codi_int)
                self.instance.carg_cbo_desc = desc_principal
        else:
            # Usuario deixou "Selecione..." / vazio → apagar ambos os campos
            cd["carg_cbo_codi"] = None
            cd["carg_cbo_desc"] = ""
            if self.instance is not None:
                self.instance.carg_cbo_codi = None
                self.instance.carg_cbo_desc = ""

        return cd
