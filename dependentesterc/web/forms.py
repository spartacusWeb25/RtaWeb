import re
from django import forms
from django.core.validators import MaxLengthValidator
from django.db import models as db_models

from dependentesterc.models import Dependentesterc
from terceiros.web.choices import CIDADES_POR_CODIGO, _choices_with_current, _current_field_value


def _only_digits(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def _cpf_valido(value):
    digits = _only_digits(value)
    if len(digits) != 11 or digits == digits[0] * 11:
        return False

    soma = sum(int(digits[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    digito_1 = 0 if resto == 10 else resto
    if digito_1 != int(digits[9]):
        return False

    soma = sum(int(digits[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    digito_2 = 0 if resto == 10 else resto
    return digito_2 == int(digits[10])


def _safe_int(v):
    if v in (None, "", [], ()):
        return None
    if isinstance(v, int):
        return v
    s = str(v).strip()
    if not s:
        return None
    s_digits = "".join(ch for ch in s if ch.isdigit())
    if not s_digits:
        return None
    try:
        return int(s_digits)
    except (TypeError, ValueError):
        return None


TIPO_DEPENDENCIA_CHOICES = [
    ("", "Selecione..."),
    (1, "01 - IR (Imposto de Renda)"),
    (2, "02 - SF (Salário Família)"),
    (3, "03 - PL (Plano de Saúde)"),
    (4, "04 - PE (Previdência)"),
    (5, "05 - PA (Pensão Alimentícia)"),
    (9, "09 - OU (Outros)"),
]

TIPO_DEPENDENTE_CHOICES = [
    ("", "Selecione..."),
    (1, "01 - Cônjuge"),
    (2, "02 - Companheiro(a) com o(a) qual tenha filho ou viva há mais de 5 anos"),
    (3, "03 - Filho(a) ou enteado(a)"),
    (4, "04 - Filho(a) ou enteado(a), universitário(a) ou cursando escola técnica de 2º grau"),
    (6, "06 - Irmão(ã), neto(a) ou bisneto(a) sem arrimo dos pais"),
    (7, "07 - Irmão(ã), neto(a) sem arrimo dos pais, universitário(a)"),
    (9, "09 - Pais, avós e bisavós"),
    (10, "10 - Menor pobre até 14 anos, sob guarda do titular"),
    (11, "11 - Incapaz/Tutelado/Curador"),
    (12, "12 - Ex-cônjuge"),
    (99, "99 - Outros"),
]


FIELD_LABELS = {
    "registro": "Registro",
    "depe_empr": "Empresa",
    "depe_fili": "Filial",
    "depe_terc": "Código do terceiro",
    "depe_codi": "Código do dependente",

    "depe_nome": "Nome",
    "depe_nascimento": "Nascimento",
    "depe_matricula": "Matrícula",
    "depe_local_nascimento": "Local de nascimento",
    "depe_cidade_codigo": "Cidade (Código IBGE)",
    "depe_cidade": "Cidade",
    "depe_cartorio": "Cartório",
    "depe_numero_registro": "Número do registro",
    "depe_numero_livro": "Número do livro",
    "depe_numero_folha": "Número da folha",
    "depe_data_entrega": "Data da entrega",
    "depe_cpf": "CPF",
    "depe_data_baixa": "Data da baixa",
    "depe_ir_ate": "Dependente IR até",
    "depe_tipo_dependente": "Tipo de dependente",
    "depe_tipo_dependente_desc": "Tipo de dependente (descrição)",
    "depe_descricao_dependencia": "Descrição da dependência",
    "depe_tipo_dependencia": "Tipo de dependência",
    "depe_invalido": "Inválido",
    "depe_observacoes": "Observações",
}


COMBO_CHOICES_FIELDS = {
    "depe_tipo_dependencia": TIPO_DEPENDENCIA_CHOICES,
}


class DependentestercForm(forms.ModelForm):
    class Meta:
        model = Dependentesterc
        fields = "__all__"
        labels = FIELD_LABELS

    _NUMERIC_SAFE_FIELDS = None

    def _init_safe_field_lists(self):
        self._NUMERIC_SAFE_FIELDS = [
            "depe_empr",
            "depe_fili",
            "depe_terc",
            "depe_codi",
            "depe_cidade_codigo",
            "depe_tipo_dependencia",
            "depe_tipo_dependente",
        ]

    def validate_unique(self):
        # --- BUGFIX: Django ModelForm valida `registro` como UNICO INDIVIDUAL
        #     por conta de primary_key=True no model. Nossa PK REAL no PostgreSQL
        #     eh COMPOSTA de 5 colunas (unique_together). Desativamos a validacao
        #     individual e substituimos por nossa checagem de PK composta.
        #     Sem isso nao eh possivel cadastrar MAIS DE 1 dependente para o mesmo
        #     CNPJ de licenca (mensagem: "Dependentesterc com este Registro ja existe")
        exclude = ["registro", "depe_empr", "depe_fili", "depe_terc", "depe_codi"]
        try:
            super().validate_unique(exclude=exclude)
        except Exception:
            pass

        # --- Valida nossa PK composta real (se todos os 5 campos tiverem valor) ---
        if self.instance and not hasattr(self.instance, "_state"):
            return
        cleaned = getattr(self, "cleaned_data", None) or {}
        reg = (cleaned.get("registro") or "").strip()
        emp = cleaned.get("depe_empr")
        fil = cleaned.get("depe_fili")
        ter = cleaned.get("depe_terc")
        cod = cleaned.get("depe_codi")
        if (
            reg
            and str(emp or "").isdigit()
            and str(fil or "").isdigit()
            and str(ter or "").isdigit()
            and str(cod or "").isdigit()
        ):
            try:
                qs = (
                    type(self.instance)
                    ._default_manager.using(getattr(self, "db_alias", None) or "default")
                    .filter(
                        registro=reg,
                        depe_empr=int(emp),
                        depe_fili=int(fil),
                        depe_terc=int(ter),
                        depe_codi=int(cod),
                    )
                )
                # Desconsidera a propria instancia em edicoes
                if self.instance.pk is not None:
                    try:
                        qs = qs.exclude(pk=self.instance.pk)
                    except Exception:
                        pass
                if qs.exists():
                    self.add_error(
                        "depe_codi",
                        "Ja existe um dependente com este codigo para este terceiro.",
                    )
            except Exception:
                pass

    def _sanitize_numeric_input_data(self, incoming_data):
        if incoming_data is None:
            return incoming_data
        self._init_safe_field_lists()
        try:
            from django.http import QueryDict as DjangoQueryDict
        except Exception:
            DjangoQueryDict = None
        try:
            data_copy = incoming_data.copy() if hasattr(incoming_data, "copy") else dict(incoming_data)
        except Exception:
            try:
                data_copy = dict(incoming_data.items())
            except Exception:
                return incoming_data
        numeric_fields = self._NUMERIC_SAFE_FIELDS or []
        for fname in numeric_fields:
            try:
                if DjangoQueryDict is not None and isinstance(data_copy, DjangoQueryDict):
                    raw = None
                    try:
                        if fname in data_copy:
                            raw = data_copy.get(fname)
                    except Exception:
                        raw = None
                    s = str(raw or "").strip()
                    if not s:
                        try:
                            data_copy[fname] = None
                        except Exception:
                            try:
                                data_copy.setlist(fname, [None])
                            except Exception:
                                pass
                elif isinstance(data_copy, dict):
                    raw = data_copy.get(fname)
                    if isinstance(raw, (list, tuple)):
                        raw = raw[0] if raw else None
                    s = str(raw or "").strip()
                    if not s:
                        data_copy[fname] = None
            except Exception:
                continue
        return data_copy

    def full_clean(self):
        if self.data is not None:
            self.data = self._sanitize_numeric_input_data(self.data)
        super().full_clean()

    def __init__(self, *args, db_alias=None, banco=None, **kwargs):
        self.db_alias = db_alias
        self.banco = banco
        if args:
            args_list = list(args)
            for i in range(len(args_list)):
                if i == 0 and args_list[i] is not None:
                    val = args_list[i]
                    is_mapping = isinstance(val, dict) or (hasattr(val, "get") and hasattr(val, "items"))
                    if is_mapping:
                        args_list[i] = self._sanitize_numeric_input_data(val)
            args = tuple(args_list)
        else:
            data_kw = kwargs.get("data")
            if data_kw is not None:
                kwargs["data"] = self._sanitize_numeric_input_data(data_kw)
        super().__init__(*args, **kwargs)

        for nome, field in self.fields.items():
            try:
                model_field = self._meta.model._meta.get_field(nome)
            except Exception:
                model_field = None

            if model_field is not None and isinstance(model_field, db_models.BooleanField):
                field.required = False
                field.widget = forms.CheckboxInput(attrs={"class": "form-check-input"})
                continue

            if model_field is not None and isinstance(model_field, db_models.DateField):
                field.widget = forms.DateInput(
                    attrs={"class": "form-control", "placeholder": "dd/mm/aaaa", "type": "date"},
                    format="%Y-%m-%d",
                )
                field.input_formats = ["%Y-%m-%d", "%d/%m/%Y"]
                continue

            if model_field is not None and isinstance(model_field, db_models.TextField):
                field.widget.attrs.setdefault("class", "form-control")
                field.widget.attrs.setdefault("rows", 6)
                continue

            if nome in COMBO_CHOICES_FIELDS:
                valor_atual = _current_field_value(self, nome)
                field.widget = forms.Select(
                    attrs={"class": "form-select"},
                    choices=_choices_with_current(COMBO_CHOICES_FIELDS[nome], valor_atual),
                )
                field.required = False
                continue

            if model_field is not None and isinstance(model_field, (db_models.IntegerField, db_models.DecimalField, db_models.FloatField)):
                widget = field.widget
                if not isinstance(widget, forms.NumberInput):
                    widget = forms.NumberInput()
                    field.widget = widget
                widget.attrs["class"] = "form-control"
                continue

            if not field.widget.attrs.get("class"):
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs.setdefault("class", "form-control")

        # --- campos CHAVE / PK COMPOSTA ---
        if "registro" in self.fields:
            self.fields["registro"].widget = forms.HiddenInput()
            self.fields["registro"].required = False

        if "depe_codi" in self.fields:
            self.fields["depe_codi"].widget = forms.HiddenInput()
            self.fields["depe_codi"].required = False

        if "depe_empr" in self.fields:
            self.fields["depe_empr"].widget = forms.HiddenInput()
            self.fields["depe_empr"].required = False

        if "depe_fili" in self.fields:
            self.fields["depe_fili"].widget = forms.HiddenInput()
            self.fields["depe_fili"].required = False

        if "depe_terc" in self.fields:
            self.fields["depe_terc"].widget = forms.HiddenInput()
            self.fields["depe_terc"].required = False

        # --- campos DESC (TODOS hidden por padrão, exceto depe_cidade visivel readonly abaixo) ---
        for desc_field in (
            "depe_tipo_dependente_desc",
            "depe_tipo_dependencia_desc",
            "depe_cidade_desc",
        ):
            if desc_field in self.fields:
                self.fields[desc_field].widget = forms.HiddenInput()
                self.fields[desc_field].required = False

        # --- Tipo dependente: COMBO full width ---
        if "depe_tipo_dependente" in self.fields:
            valor_atual = _current_field_value(self, "depe_tipo_dependente")
            self.fields["depe_tipo_dependente"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(TIPO_DEPENDENTE_CHOICES, valor_atual),
            )
            self.fields["depe_tipo_dependente"].required = False

        # --- Cidade (Código IBGE) + Cidade desc visivel readonly ---
        if "depe_cidade" in self.fields:
            field = self.fields["depe_cidade"]
            field.widget = forms.TextInput(attrs={
                "class": "form-control",
                "readonly": "readonly",
                "placeholder": "Nome da cidade preenchido automaticamente",
            })
            field.label = "Cidade"
            field.required = False
            field.validators = [
                v for v in field.validators
                if not isinstance(v, MaxLengthValidator)
            ]

        # --- Placeholders com mascaras informativas + data-mask (igual terceiros form) ---
        if "depe_cpf" in self.fields:
            field = self.fields["depe_cpf"]
            field.max_length = 14
            field.widget.attrs["maxlength"] = 14
            field.widget.attrs["data-mask"] = "cpf"
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["placeholder"] = "000.000.000-00"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "depe_numero_registro" in self.fields:
            field = self.fields["depe_numero_registro"]
            field.max_length = 20
            field.widget.attrs["maxlength"] = 20
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.widget.attrs["placeholder"] = "0000000000"
            field.required = False

        if "depe_numero_livro" in self.fields:
            field = self.fields["depe_numero_livro"]
            field.max_length = 20
            field.widget.attrs["maxlength"] = 20
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.widget.attrs["placeholder"] = "000"
            field.required = False

        if "depe_numero_folha" in self.fields:
            field = self.fields["depe_numero_folha"]
            field.max_length = 20
            field.widget.attrs["maxlength"] = 20
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.widget.attrs["placeholder"] = "0000"
            field.required = False

        if "depe_ir_ate" in self.fields:
            field = self.fields["depe_ir_ate"]
            field.max_length = 7
            field.widget.attrs["maxlength"] = 7
            field.widget.attrs["data-mask"] = "00/0000"
            field.widget.attrs["placeholder"] = "MM/AAAA"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        # --- REGRA FINAL (1:1 tela legada): TODOS os campos de dados SAO OPCIONAIS.
        #     Nenhum campo alem da PK (ja tratada acima) deve ser required=True,
        #     pois o sistema legado permitia gravar com quase tudo vazio.
        #     Isso evita o alerta amarelo "Revise os campos destacados em vermelho"
        #     com erros de "Este campo é obrigatório" em campos invisiveis / fora da tela.
        for nome, field in self.fields.items():
            if nome in ("registro", "depe_empr", "depe_fili", "depe_terc", "depe_codi"):
                continue
            field.required = False

    # --- Clean: sanitização individual ---
    def clean_depe_cpf(self):
        valor = self.cleaned_data.get("depe_cpf") or ""
        digitos = _only_digits(valor)
        if not digitos:
            return None
        if len(digitos) == 11 and not _cpf_valido(digitos):
            raise forms.ValidationError("Informe um CPF válido.")
        return digitos[:11] or None

    def clean_depe_cidade_codigo(self):
        valor = self.cleaned_data.get("depe_cidade_codigo")
        codigo_limpo = _safe_int(valor)
        if codigo_limpo and str(codigo_limpo) in CIDADES_POR_CODIGO:
            cidade = CIDADES_POR_CODIGO[str(codigo_limpo)]
            if isinstance(cidade, (list, tuple)):
                self.cleaned_data["depe_cidade"] = str(cidade[0] or "")[:60]
        return codigo_limpo

    def clean_depe_numero_registro(self):
        v = self.cleaned_data.get("depe_numero_registro")
        return (_only_digits(v)[:20]) or None

    def clean_depe_numero_livro(self):
        v = self.cleaned_data.get("depe_numero_livro")
        return (_only_digits(v)[:20]) or None

    def clean_depe_numero_folha(self):
        v = self.cleaned_data.get("depe_numero_folha")
        return (_only_digits(v)[:20]) or None

    def clean_depe_ir_ate(self):
        valor = (self.cleaned_data.get("depe_ir_ate") or "").strip()
        if not valor:
            return None
        digits = _only_digits(valor)
        if len(digits) == 6:
            return f"{digits[:2]}/{digits[2:]}"
        if re.fullmatch(r"\d{2}/\d{4}", valor):
            return valor
        return valor[:7] or None

    def clean_depe_tipo_dependente(self):
        valor = self.cleaned_data.get("depe_tipo_dependente")
        val_int = _safe_int(valor)
        if val_int:
            for codigo, desc in TIPO_DEPENDENTE_CHOICES:
                if codigo and int(codigo) == val_int:
                    self.cleaned_data["depe_tipo_dependente_desc"] = str(desc or "")[:60]
                    break
        return val_int

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("depe_invalido") in ("", None):
            cleaned["depe_invalido"] = False
        if cleaned.get("depe_cidade") and len(str(cleaned["depe_cidade"])) > 60:
            cleaned["depe_cidade"] = str(cleaned["depe_cidade"])[:60]
        return cleaned
