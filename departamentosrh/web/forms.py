from django import forms
from django.db import models

from departamentosrh.models import DepartamentosRh
from departamentosrh.services.logic import _digits_only

TIPO_DOCUMENTO_CHOICES = [
    (1, "CNPJ"),
    (2, "CEI"),
]

DADOS_CAD_PERC_CHOICES = [
    (1, "Nenhum"),
    (2, "Empresa"),
    (3, "Filial"),
    (4, "Departamento"),
]

TIPO_TOMADOR_CHOICES = [
    (115, "115 - Recolhimento ao FGTS e informações à Previdência Social"),
    (130, "130 - Trabalhadores avulsos portuários"),
    (135, "135 - Trabalhadores avulsos não portuários"),
    (150, "150 - Cessão de mão de obra / Empreitada parcial"),
    (155, "155 - Obra de construção civil - Empreitada total ou obra própria"),
    (211, "211 - Cooperados por intermédio de cooperativa de trabalho"),
    (608, "608 - Dirigente sindical"),
]

TERCEIRO_CHOICES = [
    (79, "79 - Sem convênio"),
    (507, "507 - Indústria, construção civil, transporte ferroviário, telecomunicações, oficinas etc."),
    (515, "515 - Empresas de transporte rodoviário coletivo de passageiros"),
    (523, "523 - Construção civil"),
    (531, "531 - Comércio em geral"),
    (540, "540 - Cooperativas em geral"),
    (558, "558 - Prestação de serviços em geral"),
    (566, "566 - Instituições financeiras"),
    (574, "574 - Empresas de comunicação"),
    (582, "582 - Hospitais e serviços de saúde"),
    (590, "590 - Estabelecimentos de ensino"),
    (604, "604 - Agroindústria"),
    (612, "612 - Produtor rural pessoa jurídica"),
    (639, "639 - Entidades beneficentes e isentas"),
    (647, "647 - Órgãos públicos e autarquias"),
    (655, "655 - Missões diplomáticas e organismos internacionais"),
]


FIELD_LABELS = {
    "depa_codi": "Código",
    "depa_desc": "Descrição",
    "depa_apelido": "Apelido",
    "depa_inativo": "Inativo",

    "depa_cep": "CEP",
    "depa_logr": "Logradouro",
    "depa_logr_desc": "Tipo Logradouro",
    "depa_ende": "Endereço",
    "depa_ende_nume": "Número",
    "depa_ende_comp": "Complemento",
    "depa_ende_bair": "Bairro",
    "depa_cida_codi": "Cidade",
    "depa_cida_desc": "Cidade (descrição)",
    "depa_esta": "UF",

    "depa_ddd1": "DDD",
    "depa_fone1": "Telefone",
    "depa_emai": "E-mail",

    "depa_tipo_doc": "Tipo de documento",
    "depa_cnpj": "CNPJ",
    "depa_tipo_tomador": "Tipo tomador",
    "depa_tipo_tomador_desc": "Tipo tomador (descrição)",

    # Informações mensais
    "depa_im_terc": "Terceiro",
    "depa_im_terc_desc": "Terceiro (descrição)",
    "depa_fpas_codi": "FPAS",
    "depa_fpas_desc": "FPAS (descrição)",
    "depa_fpas_perc": "% FPAS",
    "depa_cnae_codi": "CNAE/RAT 2.0",
    "depa_cnae_desc": "CNAE/RAT 2.0 (descrição)",
    "depa_cnae_perc": "% CNAE",
    "depa_fap_aliq": "Alíquota FAP",
    "depa_gps_pag_codi": "Código pagamento GPS",
    "depa_gps_pag_desc": "Pagamento GPS (descrição)",
    "depa_gps_transp_codi": "Código GPS transportador",
    "depa_gps_transp_desc": "GPS transportador (descrição)",
    "depa_dados_cad_codi": "Dados cadastrais",
    "depa_dados_perc_codi": "Dados percentuais",
    "depa_tx_servico": "Taxa de serviço",
    "depa_contab_codi": "Código na contabilidade",
    "depa_mensagens1": "Mensagens",
    "depa_mensagens2": "",

    "depa_usuario_inc": "Usuário inclusão",
    "depa_data_inc": "Data inclusão",
    "depa_usuario_alt": "Usuário alteração",
    "depa_data_alt": "Data alteração",
}


_DIGITS_ONLY_FIELDS = (
    "depa_codi",
    "depa_cep",
    "depa_logr",
    "depa_cida_codi",
    "depa_ddd1",
    "depa_im_terc",
    "depa_fpas_codi",
    "depa_cnae_codi",
    "depa_gps_pag_codi",
    "depa_gps_transp_codi",
    "depa_dados_cad_codi",
    "depa_dados_perc_codi",
    "depa_tipo_tomador",
)

_DECIMAL_2_FIELDS = {
    "depa_fpas_perc": 10,
    "depa_cnae_perc": 10,
    "depa_tx_servico": 14,
}

_DECIMAL_4_FIELDS = {
    "depa_fap_aliq": 14,
}


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


def _combo_choices_for_value(value):
    """Combo padrão para campos integer SEM choices explícitas.

    SEMPRE começa com opção (None, "Selecione") no topo, e depois
    o valor atual previamente salvo (se houver).
    """
    choices = [(None, "Selecione")]
    if value in (None, ""):
        return choices
    try:
        val_int = int(value)
    except Exception:
        val_str = str(value).strip()
        if val_str:
            choices.append((val_str, f"{val_str} (atual)"))
        return choices
    # Garante que a opção atual nao seja duplicada com o "Selecione"
    if val_int not in (None, ""):
        choices.append((val_int, f"{val_int} (atual)"))
    return choices


def _current_field_value(form, nome):
    if form.is_bound and nome in form.data:
        return form.data.get(nome)
    if nome in (form.initial or {}):
        return form.initial.get(nome)
    if getattr(form, "instance", None) is not None:
        return getattr(form.instance, nome, None)
    return None


class DepartamentoRhForm(forms.ModelForm):

    class Meta:
        model = DepartamentosRh
        fields = "__all__"
        labels = FIELD_LABELS
        widgets = {
            "registro": forms.HiddenInput(),
            "depa_empr": forms.HiddenInput(),
            "depa_fili": forms.HiddenInput(),
            "depa_codi": forms.HiddenInput(),
            "depa_desc": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: Administrativo, Financeiro...",
                "maxlength": 200,
            }),
            "depa_apelido": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Apelido / Abreviação",
                "maxlength": 100,
            }),
            "depa_inativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),

            "depa_cep": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "00000-000",
                "maxlength": 10,
                "inputmode": "numeric",
            }),
            "depa_ende": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 200,
                "placeholder": "Endereço completo (inclui tipo logradouro)",
            }),
            "depa_ende_nume": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 20,
                "placeholder": "S/N ou nº",
            }),
            "depa_ende_comp": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 80,
                "placeholder": "Sala, Andar, Bloco...",
            }),
            "depa_ende_bair": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 80,
                "placeholder": "Bairro",
            }),
            "depa_cida_desc": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 100,
                "placeholder": "Cidade",
            }),
            "depa_esta": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 2,
                "placeholder": "UF",
            }),
            "depa_ddd1": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 4,
                "placeholder": "DDD",
                "data-digits-only": "true",
            }),
            "depa_fone1": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 20,
                "placeholder": "Telefone",
            }),
            "depa_emai": forms.EmailInput(attrs={
                "class": "form-control",
                "maxlength": 120,
                "placeholder": "departamento@empresa.com.br",
            }),
            "depa_tipo_doc": forms.Select(attrs={
                "class": "form-select",
            }, choices=TIPO_DOCUMENTO_CHOICES),
            "depa_cnpj": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 18,
                "placeholder": "00.000.000/0000-00",
                "inputmode": "numeric",
            }),
            "depa_tipo_tomador_desc": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 160,
                "placeholder": "Ex.: Construção civil (155)",
            }),

            "depa_im_terc_desc": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 200,
                "placeholder": "Terceiro descrição",
            }),
            "depa_fpas_desc": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 200,
                "placeholder": "FPAS descrição",
            }),
            "depa_cnae_desc": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 250,
                "placeholder": "CNAE descrição",
            }),
            "depa_gps_pag_desc": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 220,
                "placeholder": "Pagamento GPS descrição",
            }),
            "depa_gps_transp_desc": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 220,
                "placeholder": "GPS transportador descrição",
            }),
            "depa_dados_cad_codi": forms.Select(attrs={
                "class": "form-select",
            }, choices=DADOS_CAD_PERC_CHOICES),
            "depa_dados_perc_codi": forms.Select(attrs={
                "class": "form-select",
            }, choices=DADOS_CAD_PERC_CHOICES),
            "depa_contab_codi": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 40,
                "placeholder": "Código contábil",
            }),
            "depa_mensagens1": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 255,
                "placeholder": "Mensagem linha 1",
            }),
            "depa_mensagens2": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 255,
                "placeholder": "Mensagem linha 2",
            }),
            "depa_usuario_inc": forms.HiddenInput(),
            "depa_data_inc": forms.HiddenInput(),
            "depa_usuario_alt": forms.HiddenInput(),
            "depa_data_alt": forms.HiddenInput(),
        }

    def __init__(self, *args, db_alias=None, banco=None, empr_fixo=None, fili_fixo=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_alias = db_alias or "default"
        self.banco = banco

        # Garante sempre empr=1 e fili=1 (mesmo que usuário altere hidden via inspect)
        empr_val = 1 if empr_fixo is None else int(empr_fixo)
        fili_val = 1 if fili_fixo is None else int(fili_fixo)
        self.initial["depa_empr"] = empr_val
        self.initial["depa_fili"] = fili_val
        if "depa_empr" in self.fields:
            self.fields["depa_empr"].initial = empr_val
        if "depa_fili" in self.fields:
            self.fields["depa_fili"].initial = fili_val
        self._empr_fixo = empr_val
        self._fili_fixo = fili_val

        if "depa_tipo_doc" in self.fields:
            f = self.fields["depa_tipo_doc"]
            f.choices = TIPO_DOCUMENTO_CHOICES
            f.widget = forms.RadioSelect(
                choices=TIPO_DOCUMENTO_CHOICES,
                attrs={"class": "form-check-input"},
            )
            f.coerce = int
            f.empty_value = None
            f.required = False

        if "depa_dados_cad_codi" in self.fields:
            self.fields["depa_dados_cad_codi"].choices = DADOS_CAD_PERC_CHOICES
            self.fields["depa_dados_cad_codi"].required = False
        if "depa_dados_perc_codi" in self.fields:
            self.fields["depa_dados_perc_codi"].choices = DADOS_CAD_PERC_CHOICES
            self.fields["depa_dados_perc_codi"].required = False

        # Força attr de maxlength para CEP e CNPJ ignorando o max_length do modelo
        # (pois o modelo max_length é 8/14 para salvar s/ máscara, mas na tela a
        # máscara adiciona . - / deixando 10 / 18 caracteres de digitação total)
        #
        # IMPORTANTE: setamos field.max_length = None e removemos MaxLengthValidator
        # do ModelForm pq senão o validador automático do Django roda ANTES do nosso
        # clean_xxx e acusa "no máximo 8 caracteres" mesmo com a máscara.
        from django.core.validators import MaxLengthValidator

        if "depa_cep" in self.fields:
            fc = self.fields["depa_cep"]
            # Remove o limitador do ModelForm (o nosso clean já valida com 8 digitos)
            fc.max_length = None
            fc.validators = [v for v in (fc.validators or []) if not isinstance(v, MaxLengthValidator)]
            fc.widget.attrs["maxlength"] = 11
            fc.widget.attrs["placeholder"] = "00000-000"
            fc.widget.attrs["inputmode"] = "numeric"
            fc.widget.attrs["class"] = (
                (fc.widget.attrs.get("class") or "") + " form-control"
            ).strip()
        if "depa_cnpj" in self.fields:
            fc = self.fields["depa_cnpj"]
            # Remove o limitador do ModelForm (o nosso clean já valida 14/12 digitos)
            fc.max_length = None
            fc.validators = [v for v in (fc.validators or []) if not isinstance(v, MaxLengthValidator)]
            fc.widget.attrs["maxlength"] = 20
            fc.widget.attrs["placeholder"] = "00.000.000/0000-00"
            fc.widget.attrs["inputmode"] = "numeric"
            fc.widget.attrs["class"] = (
                (fc.widget.attrs.get("class") or "") + " form-control"
            ).strip()

        for nome, field in self.fields.items():
            model_field = None
            try:
                model_field = self._meta.model._meta.get_field(nome)
            except Exception:
                model_field = None

            if model_field is not None:
                if isinstance(model_field, models.BooleanField):
                    field.required = False
                    if not isinstance(field.widget, forms.CheckboxInput):
                        field.widget = forms.CheckboxInput(attrs={"class": "form-check-input"})
                    continue
                if isinstance(model_field, models.DateTimeField):
                    field.widget = forms.DateTimeInput(
                        attrs={"class": "form-control", "type": "datetime-local"},
                        format="%Y-%m-%dT%H:%M",
                    )
                    field.input_formats = ["%Y-%m-%dT%H:%M"]
                    field.required = False
                    continue
                if isinstance(model_field, models.DateField):
                    field.widget = forms.DateInput(
                        attrs={"class": "form-control", "type": "date"},
                        format="%Y-%m-%d",
                    )
                    field.input_formats = ["%Y-%m-%d"]
                    field.required = False
                    continue

            if nome in _DIGITS_ONLY_FIELDS:
                attrs = dict(field.widget.attrs or {})
                attrs.setdefault("data-digits-only", "true")
                attrs.setdefault("inputmode", "numeric")
                if "class" not in attrs or "form-control" not in attrs["class"]:
                    attrs["class"] = (attrs.get("class", "") + " form-control").strip()
                field.widget.attrs = attrs
                field.required = False

            if nome in _DECIMAL_2_FIELDS:
                max_digits = _DECIMAL_2_FIELDS[nome]
                attrs = dict(field.widget.attrs or {})
                attrs.setdefault("class", "form-control")
                attrs.setdefault("data-decimal-2", "true")
                attrs.setdefault("inputmode", "decimal")
                attrs.setdefault("step", "0.01")
                attrs.setdefault("maxlength", str(max_digits + 2))
                field.widget = forms.NumberInput(attrs=attrs)
                field.required = False
                continue

            if nome in _DECIMAL_4_FIELDS:
                max_digits = _DECIMAL_4_FIELDS[nome]
                attrs = dict(field.widget.attrs or {})
                attrs.setdefault("class", "form-control")
                attrs.setdefault("data-decimal-4", "true")
                attrs.setdefault("inputmode", "decimal")
                attrs.setdefault("step", "0.0001")
                attrs.setdefault("maxlength", str(max_digits + 4))
                field.widget = forms.NumberInput(attrs=attrs)
                field.required = False
                continue

            # Campos integer restantes: depa_logr, depa_cida_codi, etc. -> combobox
            # depa_tipo_tomador é um caso ESPECIAL: possui choices fixas listadas pelo usuário
            if nome == "depa_tipo_tomador":
                valor_atual = _current_field_value(self, nome)
                choices = [(None, "Selecione")] + list(TIPO_TOMADOR_CHOICES)
                if valor_atual not in (None, "") and not any(
                    _safe_int(c) == _safe_int(valor_atual) for c, _ in choices
                ):
                    choices.append((valor_atual, str(valor_atual).strip()))
                field.coerce = int
                field.empty_value = None
                field.choices = choices
                field.widget = forms.Select(
                    attrs={"class": "form-select"},
                    choices=choices,
                )
                field.required = False
                continue

            # depa_im_terc é um caso ESPECIAL: Tabela 04 do eSocial - Códigos e Alíquotas de FPAS/Terceiros
            if nome == "depa_im_terc":
                valor_atual = _current_field_value(self, nome)
                choices = [(None, "Selecione")] + list(TERCEIRO_CHOICES)
                if valor_atual not in (None, "") and not any(
                    _safe_int(c) == _safe_int(valor_atual) for c, _ in choices
                ):
                    choices.append((valor_atual, str(valor_atual).strip()))
                field.coerce = int
                field.empty_value = None
                field.choices = choices
                field.widget = forms.Select(
                    attrs={"class": "form-select"},
                    choices=choices,
                )
                field.required = False
                continue

            INTEGER_COMBO = ("depa_logr", "depa_cida_codi",
                             "depa_fpas_codi", "depa_cnae_codi",
                             "depa_gps_pag_codi", "depa_gps_transp_codi")
            if nome in INTEGER_COMBO:
                valor_atual = _current_field_value(self, nome)
                field.widget = forms.Select(
                    attrs={"class": "form-select"},
                    choices=_combo_choices_for_value(valor_atual),
                )
                field.required = False
                continue

            if nome == "depa_esta":
                from funcionarios.web.choices import BRAZILIAN_UF_CHOICES
                valor_atual = _current_field_value(self, nome)
                # Converte choices do global (ex: ("PR", "PR - Paraná")) para exibir
                # SOMENTE a sigla, como o usuário pediu.
                uf_choices_sigla = []
                for codigo, rotulo in BRAZILIAN_UF_CHOICES:
                    # codigo ex: "PR", rotulo original: "PR - Paraná"
                    # Troca rótulo para ser só a sigla
                    sigla = str(codigo).strip() if codigo not in (None, "") else ""
                    if sigla:
                        uf_choices_sigla.append((codigo, sigla))
                    elif codigo in (None, ""):
                        # Pula o (None/Selecione) inicial pois nós adicionamos abaixo
                        continue
                choices = [(None, "Selecione")] + uf_choices_sigla
                if valor_atual not in (None, "") and not any(
                    (c is not None and str(c) == str(valor_atual)) or c == valor_atual
                    for c, _ in choices
                ):
                    choices.append((valor_atual, str(valor_atual).strip()))
                field.widget = forms.Select(
                    attrs={"class": "form-select"},
                    choices=choices,
                )
                field.required = False
                continue

            # Default text inputs -> class form-control
            try:
                widget = field.widget
                if not isinstance(widget, (forms.HiddenInput, forms.CheckboxInput,
                                           forms.Select, forms.SelectMultiple,
                                           forms.NumberInput)):
                    if "class" not in (widget.attrs or {}) or "form-control" not in str(widget.attrs.get("class", "")):
                        attrs = dict(widget.attrs or {})
                        attrs["class"] = (attrs.get("class", "") + " form-control").strip()
                        widget.attrs = attrs
            except Exception:
                pass

            if nome.startswith("depa_") and nome not in ("depa_desc",):
                field.required = False

        if "depa_inativo" in self.fields:
            self.fields["depa_inativo"].required = False

    # --- cleans PK e integer fields ---
    def clean_depa_empr(self):
        return _safe_int(self.cleaned_data.get("depa_empr"))

    def clean_depa_fili(self):
        return _safe_int(self.cleaned_data.get("depa_fili"))

    def clean_depa_codi(self):
        return _safe_int(self.cleaned_data.get("depa_codi"))

    def clean_depa_logr(self):
        return _safe_int(self.cleaned_data.get("depa_logr"))

    def clean_depa_cida_codi(self):
        return _safe_int(self.cleaned_data.get("depa_cida_codi"))

    def clean_depa_im_terc(self):
        v = _safe_int(self.cleaned_data.get("depa_im_terc"))
        if v is None:
            return None
        codigos_validos = {cod for cod, _ in TERCEIRO_CHOICES}
        if v in codigos_validos:
            return v
        try:
            v_int = int(v)
        except (TypeError, ValueError):
            return None
        if v_int < 0:
            return None
        if v_int > 9999:
            v_int = int(str(v_int)[:4]) or None
        return v_int

    def clean_depa_fpas_codi(self):
        return _safe_int(self.cleaned_data.get("depa_fpas_codi"))

    def clean_depa_cnae_codi(self):
        return _safe_int(self.cleaned_data.get("depa_cnae_codi"))

    def clean_depa_gps_pag_codi(self):
        return _safe_int(self.cleaned_data.get("depa_gps_pag_codi"))

    def clean_depa_gps_transp_codi(self):
        return _safe_int(self.cleaned_data.get("depa_gps_transp_codi"))

    def clean_depa_empr(self):
        return int(getattr(self, "_empr_fixo", 1) or 1)

    def clean_depa_fili(self):
        return int(getattr(self, "_fili_fixo", 1) or 1)

    def clean_depa_tipo_doc(self):
        v = _safe_int(self.cleaned_data.get("depa_tipo_doc"))
        if v is None:
            return 1
        if v not in (1, 2):
            return 1
        return v

    def clean_depa_tipo_tomador(self):
        v = _safe_int(self.cleaned_data.get("depa_tipo_tomador"))
        if v is None:
            return None
        # Garante apenas códigos válidos da lista (max 3 dígitos, entre 1-999)
        codigos_validos = {cod for cod, _ in TIPO_TOMADOR_CHOICES}
        if v in codigos_validos:
            return v
        # Se o usuario inseriu algo manual, aceita mas corta em 999
        try:
            v_int = int(v)
        except (TypeError, ValueError):
            return None
        if v_int < 0:
            return None
        if v_int > 999:
            v_int = int(str(v_int)[:3]) or None
        return v_int

    def clean_depa_cnpj(self):
        v = self.cleaned_data.get("depa_cnpj")
        if v in (None, ""):
            return None
        digits = _digits_only(v) or ""
        tipo_doc = _safe_int(self.cleaned_data.get("depa_tipo_doc"))
        if tipo_doc == 2:
            # CEI = 12 dígitos
            digits = digits[:12]
        else:
            # CNPJ = 14 dígitos
            digits = digits[:14]
        return digits or None

    def clean_depa_dados_cad_codi(self):
        v = _safe_int(self.cleaned_data.get("depa_dados_cad_codi"))
        if v is None:
            return 1
        return v

    def clean_depa_dados_perc_codi(self):
        v = _safe_int(self.cleaned_data.get("depa_dados_perc_codi"))
        if v is None:
            return 1
        return v

    def clean_depa_cep(self):
        v = self.cleaned_data.get("depa_cep")
        if v in (None, ""):
            return None
        return _digits_only(v)[:8] or None

    def clean_depa_ddd1(self):
        v = self.cleaned_data.get("depa_ddd1")
        if v in (None, ""):
            return None
        return _digits_only(v)[:4] or None

    def validate_unique(self):
        banco_limpo = _digits_only(self.banco or "")
        empr = _safe_int(self.cleaned_data.get("depa_empr"))
        fili = _safe_int(self.cleaned_data.get("depa_fili"))
        codi = _safe_int(self.cleaned_data.get("depa_codi"))

        if not all([banco_limpo, empr, fili, codi]):
            return

        qs = DepartamentosRh.objects.using(self.db_alias).filter(
            registro=banco_limpo,
            depa_empr=int(empr),
            depa_fili=int(fili),
            depa_codi=int(codi),
        )

        instance = getattr(self, "instance", None)
        is_editar = False
        if instance is not None:
            try:
                pk_parts = (
                    getattr(instance, "registro", None),
                    getattr(instance, "depa_empr", None),
                    getattr(instance, "depa_fili", None),
                    getattr(instance, "depa_codi", None),
                )
                is_editar = all(v is not None for v in pk_parts)
            except Exception:
                is_editar = False
        if is_editar:
            qs = qs.exclude(
                registro=getattr(instance, "registro"),
                depa_empr=getattr(instance, "depa_empr"),
                depa_fili=getattr(instance, "depa_fili"),
                depa_codi=getattr(instance, "depa_codi"),
            )

        if qs.exists():
            self.add_error(
                "depa_codi",
                f"Já existe um Departamento cadastrado com o Código {codi} "
                f"para a Empresa/Filial selecionada."
            )

    def clean(self):
        cd = super().clean() or {}
        if not cd.get("depa_desc"):
            self.add_error("depa_desc", "O campo Descrição do departamento é obrigatório.")

        # Sincroniza automaticamente depa_im_terc_desc com a descrição de TERCEIRO_CHOICES
        terc_cod = cd.get("depa_im_terc")
        if terc_cod is not None:
            mapa_terceiro = {int(cod): desc for cod, desc in TERCEIRO_CHOICES}
            try:
                desc = mapa_terceiro.get(int(terc_cod))
                if desc and ("depa_im_terc_desc" in cd):
                    cd["depa_im_terc_desc"] = desc
            except (TypeError, ValueError):
                pass

        return cd
