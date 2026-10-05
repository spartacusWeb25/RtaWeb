from django import forms
from datetime import date

from prepara_recisoes.models import PreparaRescisoes


# ==============================================================================
# CHOICES DAS COMBOBOXES (Destacadas no print, o usuario pode add mais depois!)
# 1a opcao SEMPRE = "Selecione"  (valor vazio -> obrigatorio selecionar se quiser)
# ==============================================================================
CHOICES_INICIATIVA = [
    ("", "Selecione"),
    (1,  "Empresa"),
    (2,  "Empregado"),
    (3,  "Pedido mútuo acordo"),
    (4,  "Justa causa"),
    (5,  "Sem justa causa"),
    (6,  "Falecimento"),
]

CHOICES_AVISO_PREVIO = [
    ("", "Selecione"),
    (1,  "Indenizado"),
    (2,  "Trabalhado"),
    (3,  "Sem Aviso"),
    (4,  "S/Data"),
    (5,  "Dispensado sem justa causa"),
    (6,  "Dispensado com justa causa"),
]

CHOICES_GFD = [
    ("", "Selecione"),
    (1,  "Guia FGTS Digital (Mensal) / Exporta GFIP"),
    (2,  "Conforme tipo de afastamento do colaborador"),
    (3,  "Não informar em GFD (Somente GPS SEFIP)"),
]

# Dicts auxiliares para AUTO-PREENCHIMENTO do campo _desc correspondente
# (a combobox grava o CODIGO integer no _codi; o texto no _desc)
_MAP_INICIATIVA_DESC    = {cod: desc for (cod, desc) in CHOICES_INICIATIVA if cod != ""}
_MAP_AVISO_PREVIO_DESC  = {cod: desc for (cod, desc) in CHOICES_AVISO_PREVIO  if cod != ""}
_MAP_GFD_DESC           = {cod: desc for (cod, desc) in CHOICES_GFD           if cod != ""}


FIELD_LABELS = {
    "prep_codi": "Código",
    "prep_desc": "Descrição (título)",
    "prep_descricao": "Descrição",
    "prep_inativo": "Inativo",

    # --- Dados Gerais ---
    "prep_iniciativa_codi": "Iniciativa",
    "prep_iniciativa_desc": "Iniciativa (descrição)",
    "prep_aviso_previo_codi": "Aviso prévio",
    "prep_aviso_previo_desc": "Aviso prévio (descrição)",
    "prep_inden_ferias_13": "Indenização 1/12 de férias e 13º",

    "prep_saque_codi": "Código saque",
    "prep_saque_desc": "Código saque (descrição)",

    "prep_fgts_codi": "FGTS",
    "prep_fgts_desc": "FGTS (descrição)",
    "prep_fgts_int_codi": "FGTS intermitente",
    "prep_fgts_int_desc": "FGTS intermitente (descrição)",

    "prep_caged_codi": "CAGED",
    "prep_caged_desc": "CAGED (descrição)",
    "prep_rais_codi": "RAIS",
    "prep_rais_desc": "RAIS (descrição)",

    "prep_gfd_codi": "GFD / GRRF",
    "prep_gfd_desc": "GFD / GRRF (descrição)",
    "prep_homolognet_codi": "Código HomologNet",
    "prep_homolognet_desc": "HomologNet (descrição)",
    "prep_motivo_esocial_codi": "Motivo eSocial",
    "prep_motivo_esocial_desc": "Motivo eSocial (descrição)",

    # --- Checkboxes ---
    "prep_justa_causa": "Justa causa",
    "prep_inden_contr_exp": "Indenização contrato experiência",
    "prep_emitir_seg_desemp": "Emitir seguro desemprego",
    "prep_50_aviso_inden": "50% do aviso indenizado",
    "prep_estabilidade": "Estabilidade",
    "prep_nao_calc_multa_resc": "Não calcula multa rescisória",
    "prep_50_verbas_inden": "50% das verbas indenizadas (aviso/férias/13º)",
    "prep_rescisao_fixa": "Rescisão fixa",

    "prep_usuario_inc": "Usuário inclusão",
    "prep_data_inc": "Data inclusão",
    "prep_usuario_alt": "Usuário alteração",
    "prep_data_alt": "Data alteração",
}

_DIGITS_ONLY_FIELDS = (
    "prep_codi",
)


def _safe_int(value):
    try:
        if value is None:
            return None
        s = str(value).strip()
        if not s or not s.isdigit():
            return None
        return int(s)
    except Exception:
        return None


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


class PreparaRescisoesForm(forms.ModelForm):

    class Meta:
        model = PreparaRescisoes
        fields = "__all__"
        labels = FIELD_LABELS
        widgets = {
            "registro": forms.HiddenInput(),
            "prep_empr": forms.HiddenInput(),
            "prep_fili": forms.HiddenInput(),
            "prep_codi": forms.HiddenInput(),

            "prep_desc": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Ex.: Falecimento com mais de 1 ano",
                    "maxlength": 200,
                }
            ),
            "prep_descricao": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Ex.: Falecimento com mais de 1 ano",
                    "maxlength": 200,
                }
            ),
            "prep_inativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),

            # --- Iniciativa + Aviso Prévio (COMBOBOXES: Select 1 unico campo) ---
            #     Codigo grava no _codi integer, o texto (descricao) é auto
            #     preenchido via clean() + hidden input _desc.
            "prep_iniciativa_codi": forms.Select(
                attrs={"class": "form-select form-select-sm", "data-desc-target": "id_prep_iniciativa_desc"},
                choices=CHOICES_INICIATIVA,
            ),
            "prep_iniciativa_desc": forms.HiddenInput(attrs={"data-auto-fill-from-combo": "true"}),
            "prep_aviso_previo_codi": forms.Select(
                attrs={"class": "form-select form-select-sm", "data-desc-target": "id_prep_aviso_previo_desc"},
                choices=CHOICES_AVISO_PREVIO,
            ),
            "prep_aviso_previo_desc": forms.HiddenInput(attrs={"data-auto-fill-from-combo": "true"}),
            "prep_inden_ferias_13": forms.CheckboxInput(attrs={"class": "form-check-input"}),

            # --- Código Saque FGTS ---
            "prep_saque_codi": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm text-center",
                    "maxlength": 20,
                }
            ),
            "prep_saque_desc": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Ex.: Rescisão contratual por falecimento",
                    "maxlength": 200,
                }
            ),

            # --- FGTS e FGTS Intermitente ---
            "prep_fgts_codi": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm text-center",
                    "maxlength": 20,
                }
            ),
            "prep_fgts_desc": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Ex.: Falecimento",
                    "maxlength": 200,
                }
            ),
            "prep_fgts_int_codi": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm text-center",
                    "maxlength": 20,
                }
            ),
            "prep_fgts_int_desc": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Ex.: Rescisão acordo contrato intermitente",
                    "maxlength": 200,
                }
            ),

            # --- CAGED / RAIS ---
            "prep_caged_codi": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm text-center",
                    "maxlength": 20,
                }
            ),
            "prep_caged_desc": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "maxlength": 200, "placeholder": "Ex.: Morte"}
            ),
            "prep_rais_codi": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm text-center",
                    "maxlength": 20,
                }
            ),
            "prep_rais_desc": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "maxlength": 200, "placeholder": "Ex.: Falecimento."}
            ),

            # --- GFD / HomologNet / Motivo eSocial (GFD = combobox! o resto input cod+desc) ---
            "prep_gfd_codi": forms.Select(
                attrs={"class": "form-select form-select-sm", "data-desc-target": "id_prep_gfd_desc"},
                choices=CHOICES_GFD,
            ),
            "prep_gfd_desc": forms.HiddenInput(attrs={"data-auto-fill-from-combo": "true"}),
            "prep_homolognet_codi": forms.TextInput(
                attrs={"class": "form-control form-control-sm text-center", "maxlength": 20}
            ),
            "prep_homolognet_desc": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "maxlength": 250,
                    "placeholder": "Ex.: Rescisão do contrato de trabalho por falecimento do empregado",
                }
            ),
            "prep_motivo_esocial_codi": forms.TextInput(
                attrs={"class": "form-control form-control-sm text-center", "maxlength": 20}
            ),
            "prep_motivo_esocial_desc": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "maxlength": 250,
                    "placeholder": "Ex.: Rescisão por falecimento do empregado",
                }
            ),

            # --- Checkboxes (booleans) ---
            "prep_justa_causa": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_inden_contr_exp": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_emitir_seg_desemp": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_50_aviso_inden": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_estabilidade": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_nao_calc_multa_resc": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_50_verbas_inden": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "prep_rescisao_fixa": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, db_alias=None, banco=None, empr_fixo=1, fili_fixo=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_alias = db_alias or "default"
        self.banco = banco
        self.empr_fixo = int(empr_fixo or 1)
        self.fili_fixo = int(fili_fixo or 1)

        for fname in _DIGITS_ONLY_FIELDS:
            if fname in self.fields:
                f = self.fields[fname]
                attrs = dict(f.widget.attrs or {})
                attrs.setdefault("data-digits-only", "true")
                attrs.setdefault("inputmode", "numeric")
                f.widget.attrs = attrs

        # Todos campos opcionais (exceto registro/empr/fili/codi que são Hidden + PK)
        for fname, field in self.fields.items():
            if fname.startswith("prep_") and fname not in ("prep_inativo",):
                field.required = False

        if "prep_inativo" in self.fields:
            self.fields["prep_inativo"].required = False

    def clean_prep_codi(self):
        valor = self.cleaned_data.get("prep_codi")
        return _safe_int(valor)

    def clean_prep_iniciativa_codi(self):
        # Combobox Select: valor chega como str "1" / "2" / "" (selecionar = vazio)
        return _safe_int(self.cleaned_data.get("prep_iniciativa_codi"))

    def clean_prep_aviso_previo_codi(self):
        return _safe_int(self.cleaned_data.get("prep_aviso_previo_codi"))

    def clean_prep_gfd_codi(self):
        return _safe_int(self.cleaned_data.get("prep_gfd_codi"))

    def validate_unique(self):
        banco_limpo = _digits_only(self.banco or "")
        empr = self.empr_fixo or _safe_int(self.cleaned_data.get("prep_empr")) or 1
        fili = self.fili_fixo or _safe_int(self.cleaned_data.get("prep_fili")) or 1
        codi = _safe_int(self.cleaned_data.get("prep_codi")) or _safe_int(self.initial.get("prep_codi"))

        if not (banco_limpo and empr and fili and codi):
            return

        from prepara_recisoes.models import PreparaRescisoes
        qs = PreparaRescisoes.objects.using(self.db_alias).filter(
            registro=banco_limpo,
            prep_empr=int(empr),
            prep_fili=int(fili),
            prep_codi=int(codi),
        )
        instance = getattr(self, "instance", None)
        is_editar = False
        if instance is not None:
            try:
                is_editar = all(getattr(instance, f, None) is not None for f in (
                    "registro", "prep_empr", "prep_fili", "prep_codi"
                ))
            except Exception:
                is_editar = False
        if is_editar:
            try:
                qs = qs.exclude(
                    registro=getattr(instance, "registro"),
                    prep_empr=getattr(instance, "prep_empr"),
                    prep_fili=getattr(instance, "prep_fili"),
                    prep_codi=getattr(instance, "prep_codi"),
                )
            except Exception:
                pass

        try:
            duplicado = qs.exists()
        except Exception:
            # Caso a tabela ainda não exista no Postgres (ainda não rodou o SQL),
            # pula a validação de duplicidade sem crashar.
            duplicado = False

        if duplicado:
            self.add_error(
                "prep_codi",
                f"Já existe uma Preparação de Rescisão com o Código {codi} para a Empresa/Filial selecionada.",
            )

    def clean(self):
        cd = super().clean() or {}
        today = date.today()
        if self.instance is not None:
            # Preenche automaticamente empresa/filial fixa no modo criar
            if not getattr(self.instance, "prep_empr", None):
                self.instance.prep_empr = self.empr_fixo
            if not getattr(self.instance, "prep_fili", None):
                self.instance.prep_fili = self.fili_fixo

        # ==============================================================
        # AUTO-PREENCHIMENTO: descrições das 3 comboboxes (iniciativa /
        # aviso previo / GFD) a partir do CODIGO selecionado no Select.
        # Grava o TEXTO no campo _desc correspondente (mantemos _desc
        # no banco igual o screenshot SCI, pra manter rastreabilidade.)
        # ==============================================================
        _auto = (
            ("prep_iniciativa_codi",    "prep_iniciativa_desc",    _MAP_INICIATIVA_DESC),
            ("prep_aviso_previo_codi",  "prep_aviso_previo_desc",  _MAP_AVISO_PREVIO_DESC),
            ("prep_gfd_codi",           "prep_gfd_desc",           _MAP_GFD_DESC),
        )
        for cod_key, desc_key, mapa in _auto:
            codi = cd.get(cod_key)
            if codi is not None and codi != "":
                try:
                    cod_int = int(codi)
                except (TypeError, ValueError):
                    cod_int = None
                desc = mapa.get(cod_int, "") if cod_int is not None else ""
                if desc:
                    cd[desc_key] = desc
                    if self.instance is not None:
                        setattr(self.instance, desc_key, desc)
            elif not cd.get(desc_key):
                cd[desc_key] = ""
                if self.instance is not None:
                    setattr(self.instance, desc_key, "")

        # Preenchimento automático de inicial prep_descricao para prep_desc
        # (se um estiver vazio e o outro não)
        if cd is not None:
            d = cd.get("prep_desc")
            dc = cd.get("prep_descricao")
            if d and not dc:
                cd["prep_descricao"] = str(d).strip()
                if self.instance is not None:
                    self.instance.prep_descricao = str(d).strip()
            elif dc and not d:
                cd["prep_desc"] = str(dc).strip()
                if self.instance is not None:
                    self.instance.prep_desc = str(dc).strip()
            # Garante valores padrão para bools
            for b in ("prep_inativo", "prep_inden_ferias_13",
                      "prep_justa_causa", "prep_inden_contr_exp",
                      "prep_emitir_seg_desemp", "prep_50_aviso_inden",
                      "prep_estabilidade", "prep_nao_calc_multa_resc",
                      "prep_50_verbas_inden", "prep_rescisao_fixa"):
                if b not in cd or cd.get(b) in (None, ""):
                    cd[b] = False
                    if self.instance is not None:
                        setattr(self.instance, b, False)
        return cd
