import re
from django import forms
from django.core.validators import MaxLengthValidator, EmailValidator
from django.db import models as db_models

from sindicatospatronais.models import SindicatosPatronais
from terceiros.web.choices import (
    TIPO_LOGRADOURO_CHOICES,
    UF_CHOICES,
    CIDADES_POR_CODIGO,
    _choices_with_current,
    _current_field_value,
)


def _only_digits(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def _cnpj_valido(value):
    digits = _only_digits(value)
    if len(digits) != 14 or digits == digits[0] * 14:
        return False

    soma = sum(int(digits[i]) * (5 - i if i < 4 else 13 - i) for i in range(12))
    resto = soma % 11
    digito_1 = 0 if resto < 2 else 11 - resto
    if digito_1 != int(digits[12]):
        return False

    soma = sum(int(digits[i]) * (6 - i if i < 5 else 14 - i) for i in range(13))
    resto = soma % 11
    digito_2 = 0 if resto < 2 else 11 - resto
    return digito_2 == int(digits[13])


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


TIPO_ENTIDADE_CHOICES = (
    ("", "Selecione"),
    (1, "Sindicato"),
    (2, "Associação"),
    (3, "Federação"),
    (4, "Confederação"),
    (5, "Outros"),
)


COMBO_CHOICES_FIELDS = {
    "sind_logr": TIPO_LOGRADOURO_CHOICES,
    "sind_esta": UF_CHOICES,
    "sind_tipo_entidade": TIPO_ENTIDADE_CHOICES,
}


FIELD_LABELS = {
    "registro": "Registro",
    "sind_empr": "Empresa",
    "sind_fili": "Filial",
    "sind_codi": "Código",
    "sind_nome": "Sindicato",
    "sind_tipo_entidade": "Entidade",
    "sind_entidade": "Entidade",
    "sind_codi_sind": "Código entidade",
    "sind_agencia_grcs": "Agência GRCS",
    "sind_codi_cede": "Código cedente",
    "sind_cep": "CEP",
    "sind_logr": "Logradouro",
    "sind_ende": "Endereço",
    "sind_ende_nume": "Número",
    "sind_ende_comp": "Complemento",
    "sind_ende_bair": "Bairro",
    "sind_cida_codi": "Cidade (Código IBGE)",
    "sind_cida_desc": "Cidade",
    "sind_esta": "UF",
    "sind_ddd1": "DDD 1",
    "sind_fone1": "Telefone 1",
    "sind_ddd2": "DDD 2",
    "sind_fone2": "Telefone 2",
    "sind_cnpj": "CNPJ",
    "sind_tabela": "Tabela",
    "sind_site": "Site",
    "sind_emai": "E-mail",
    "field_log_data": "Data log",
    "field_log_time": "Hora log",
}


class SindicatosPatronaisForm(forms.ModelForm):

    class Meta:
        model = SindicatosPatronais
        fields = "__all__"
        labels = FIELD_LABELS

    _NUMERIC_SAFE_FIELDS = None
    _DECIMAL_SAFE_FIELDS = None
    _DIGITS_ONLY_FIELDS = (
        "sind_codi_sind",
        "sind_agencia_grcs",
        "sind_codi_cede",
        "sind_ende_nume",
        "sind_tabela",
    )

    def validate_unique(self):
        exclude = ["registro", "sind_empr", "sind_fili", "sind_codi"]
        try:
            super().validate_unique(exclude=exclude)
        except Exception:
            pass
        cleaned = getattr(self, "cleaned_data", None) or {}
        reg = (cleaned.get("registro") or "").strip()
        emp = cleaned.get("sind_empr")
        fil = cleaned.get("sind_fili")
        cod = cleaned.get("sind_codi")
        if (
            reg
            and str(emp or "").isdigit()
            and str(fil or "").isdigit()
            and str(cod or "").isdigit()
        ):
            try:
                qs = (
                    type(self.instance)
                    ._default_manager.using(getattr(self, "db_alias", None) or "default")
                    .filter(
                        registro=reg,
                        sind_empr=int(emp),
                        sind_fili=int(fil),
                        sind_codi=int(cod),
                    )
                )
                if self.instance.pk is not None:
                    try:
                        qs = qs.exclude(pk=self.instance.pk)
                    except Exception:
                        pass
                if qs.exists():
                    self.add_error(
                        "sind_codi",
                        "Ja existe um sindicato patronal com este codigo e filial nesta licenca.",
                    )
            except Exception:
                pass

    def _init_safe_field_lists(self):
        self._NUMERIC_SAFE_FIELDS = [
            "sind_tipo_entidade",
            "sind_agencia_grcs",
            "sind_logr",
            "sind_cida_codi",
            "sind_tabela",
        ]
        self._DECIMAL_SAFE_FIELDS = [
        ]

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
        decimal_fields = self._DECIMAL_SAFE_FIELDS or []
        all_safe = list(numeric_fields) + list(decimal_fields)
        for fname in all_safe:
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

    def __init__(self, *args, **kwargs):
        self.db_alias = kwargs.pop("db_alias", None)
        self.banco = kwargs.pop("banco", None)
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

            if model_field is not None and isinstance(model_field, db_models.DateTimeField):
                field.widget = forms.DateTimeInput(
                    attrs={"class": "form-control", "type": "datetime-local"},
                    format="%Y-%m-%dT%H:%M",
                )
                field.input_formats = ["%Y-%m-%dT%H:%M"]
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
                field.widget.attrs.setdefault("rows", 3)
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
                if isinstance(model_field, db_models.DecimalField):
                    widget.attrs.setdefault("step", "0.01")
                continue

            if model_field is not None and isinstance(model_field, db_models.BinaryField):
                field.required = False
                field.widget = forms.FileInput(attrs={"class": "form-control", "accept": "image/*"})
                continue

            if not field.widget.attrs.get("class"):
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs.setdefault("class", "form-control")

            if nome in self._DIGITS_ONLY_FIELDS:
                field.widget.attrs.setdefault("data-digits-only", "true")
                field.widget.attrs.setdefault("inputmode", "numeric")

        if "registro" in self.fields:
            self.fields["registro"].widget = forms.HiddenInput()
            self.fields["registro"].required = False

        if "sind_empr" in self.fields:
            self.fields["sind_empr"].required = True
            self.fields["sind_empr"].label = "Empresa"
            self.fields["sind_empr"].widget.attrs["readonly"] = "readonly"

        if "sind_fili" in self.fields:
            self.fields["sind_fili"].required = True
            self.fields["sind_fili"].label = "Filial"
            self.fields["sind_fili"].widget.attrs["readonly"] = "readonly"

        if "field_log_data" in self.fields:
            self.fields["field_log_data"].widget = forms.HiddenInput()
            self.fields["field_log_data"].required = False

        if "field_log_time" in self.fields:
            self.fields["field_log_time"].widget = forms.HiddenInput()
            self.fields["field_log_time"].required = False

        if "sind_cida_desc" in self.fields:
            field = self.fields["sind_cida_desc"]
            field.widget = forms.TextInput(attrs={
                "class": "form-control",
                "readonly": "readonly",
                "placeholder": "Nome da cidade preenchido automaticamente",
            })
            field.required = False
            field.label = "Cidade"
            field.validators = [
                v for v in field.validators
                if not isinstance(v, MaxLengthValidator)
            ]

        if "sind_nome" in self.fields:
            field = self.fields["sind_nome"]
            field.widget.attrs["placeholder"] = "Nome do sindicato patronal"
            field.widget.attrs["maxlength"] = 200
            field.required = False

        if "sind_entidade" in self.fields:
            field = self.fields["sind_entidade"]
            field.widget.attrs["placeholder"] = "ex: PATRONAL"
            field.widget.attrs["maxlength"] = 20
            field.required = False
        if "sind_codi_sind" in self.fields:
            field = self.fields["sind_codi_sind"]
            field.max_length = 15
            field.widget.attrs["maxlength"] = 15
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "sind_codi_cede" in self.fields:
            field = self.fields["sind_codi_cede"]
            field.max_length = 15
            field.widget.attrs["maxlength"] = 15
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "sind_cep" in self.fields:
            field = self.fields["sind_cep"]
            field.max_length = 9
            field.widget.attrs["maxlength"] = 9
            field.widget.attrs["data-mask"] = "cep"
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.widget.attrs["placeholder"] = "00000-000"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "sind_ende" in self.fields:
            field = self.fields["sind_ende"]
            field.widget.attrs["maxlength"] = 120
            field.required = False

        if "sind_ende_nume" in self.fields:
            field = self.fields["sind_ende_nume"]
            field.widget.attrs["maxlength"] = 20
            field.required = False

        if "sind_ende_comp" in self.fields:
            field = self.fields["sind_ende_comp"]
            field.widget.attrs["maxlength"] = 60
            field.required = False

        if "sind_ende_bair" in self.fields:
            field = self.fields["sind_ende_bair"]
            field.widget.attrs["maxlength"] = 60
            field.required = False

        if "sind_ddd1" in self.fields:
            field = self.fields["sind_ddd1"]
            field.max_length = 4
            field.widget.attrs["maxlength"] = 4
            field.widget.attrs["data-mask"] = "ddd"
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["placeholder"] = "00"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "sind_fone1" in self.fields:
            field = self.fields["sind_fone1"]
            field.max_length = 20
            field.widget.attrs["maxlength"] = 20
            field.widget.attrs["data-mask"] = "telefone"
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.widget.attrs["placeholder"] = "0000-0000"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "sind_ddd2" in self.fields:
            field = self.fields["sind_ddd2"]
            field.max_length = 4
            field.widget.attrs["maxlength"] = 4
            field.widget.attrs["data-mask"] = "ddd"
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["placeholder"] = "00"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "sind_fone2" in self.fields:
            field = self.fields["sind_fone2"]
            field.max_length = 20
            field.widget.attrs["maxlength"] = 20
            field.widget.attrs["data-mask"] = "telefone"
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["placeholder"] = "0000-0000"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "sind_cnpj" in self.fields:
            field = self.fields["sind_cnpj"]
            field.max_length = 18
            field.widget.attrs["maxlength"] = 18
            field.widget.attrs["data-mask"] = "cnpj"
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["placeholder"] = "00.000.000/0000-00"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "sind_tabela" in self.fields:
            field = self.fields["sind_tabela"]
            field.widget.attrs["placeholder"] = "ex: 4"
            field.required = False

        if "sind_site" in self.fields:
            field = self.fields["sind_site"]
            field.widget.attrs["maxlength"] = 150
            field.widget.attrs["placeholder"] = "www.exemplo.com.br"
            field.required = False

        if "sind_emai" in self.fields:
            field = self.fields["sind_emai"]
            field.widget.attrs["maxlength"] = 100
            field.widget.attrs["placeholder"] = "exemplo@email.com"
            field.widget.attrs["type"] = "email"
            if not any(isinstance(v, EmailValidator) for v in field.validators):
                field.validators.append(EmailValidator())
            field.required = False

        if "sind_cida_codi" in self.fields:
            valor_atual = _current_field_value(self, "sind_cida_codi")
            self.fields["sind_cida_codi"] = forms.CharField(
                label="Cidade (Código IBGE)",
                required=False,
                max_length=160,
                widget=forms.TextInput(attrs={
                    "class": "form-control",
                    "list": "dl_cidades_ibge",
                    "placeholder": "Digite o código IBGE ou o nome da cidade/UF...",
                    "autocomplete": "off",
                })
            )
            if valor_atual not in (None, ""):
                try:
                    cod_num = _safe_int(valor_atual)
                    if cod_num is not None:
                        par = CIDADES_POR_CODIGO.get(cod_num)
                        if par:
                            nome, uf = par
                            self.initial["sind_cida_codi"] = f"{cod_num:07d} — {nome} / {uf}"
                        else:
                            self.initial["sind_cida_codi"] = f"{cod_num:07d} — {cod_num}"
                except (TypeError, ValueError):
                    pass

    def clean_sind_tabela(self):
        return _safe_int(self.cleaned_data.get("sind_tabela"))

    def clean_sind_agencia_grcs(self):
        return _safe_int(self.cleaned_data.get("sind_agencia_grcs"))

    def clean_sind_ende_nume(self):
        valor = (self.cleaned_data.get("sind_ende_nume") or "").strip()
        return _only_digits(valor)[:20] or None

    def clean_sind_cnpj(self):
        valor = (self.cleaned_data.get("sind_cnpj") or "").strip()
        digits = _only_digits(valor)[:14]
        if digits and not _cnpj_valido(digits):
            raise forms.ValidationError("Informe um CNPJ válido.")
        return digits or None

    def clean_sind_cep(self):
        valor = (self.cleaned_data.get("sind_cep") or "").strip()
        digits = _only_digits(valor)[:8]
        if digits and len(digits) != 8:
            raise forms.ValidationError("Informe um CEP válido com 8 dígitos.")
        return digits or None

    def clean_sind_ddd1(self):
        return _only_digits(self.cleaned_data.get("sind_ddd1"))[:4] or None

    def clean_sind_fone1(self):
        return _only_digits(self.cleaned_data.get("sind_fone1"))[:20] or None

    def clean_sind_ddd2(self):
        return _only_digits(self.cleaned_data.get("sind_ddd2"))[:4] or None

    def clean_sind_fone2(self):
        return _only_digits(self.cleaned_data.get("sind_fone2"))[:20] or None

    def clean_sind_codi_sind(self):
        valor = (self.cleaned_data.get("sind_codi_sind") or "").strip()
        return _only_digits(valor)[:15] or None

    def clean_sind_codi_cede(self):
        valor = (self.cleaned_data.get("sind_codi_cede") or "").strip()
        return _only_digits(valor)[:15] or None

    def clean_sind_cida_codi(self):
        valor = self.cleaned_data.get("sind_cida_codi")
        if valor in (None, ""):
            return None
        valor_str = str(valor).strip()
        match_codigo = None
        apenas_digitos = "".join(ch for ch in valor_str if ch.isdigit())
        if len(apenas_digitos) >= 2:
            try:
                match_codigo = int(apenas_digitos)
            except (TypeError, ValueError):
                match_codigo = None
        if match_codigo is not None and match_codigo in CIDADES_POR_CODIGO:
            nome, uf = CIDADES_POR_CODIGO[match_codigo]
            self.cleaned_data["sind_cida_desc"] = f"{nome} / {uf}"
            return match_codigo
        if match_codigo is not None and 1 <= len(apenas_digitos) <= 7:
            self.cleaned_data["sind_cida_desc"] = str(match_codigo)
            return match_codigo
        texto_busca = valor_str.lower()
        if texto_busca:
            for cod_num, (n, u) in CIDADES_POR_CODIGO.items():
                l1 = f"{cod_num:07d} — {n} / {u}".lower()
                l2 = f"{n} {u}".lower()
                l3 = f"{n}/{u}".lower()
                if (texto_busca in l1) or (texto_busca in l2) or (texto_busca in l3):
                    self.cleaned_data["sind_cida_desc"] = f"{n} / {u}"
                    return cod_num
        raise forms.ValidationError(
            "Cidade não encontrada. Digite o código IBGE de 7 dígitos "
            "ou comece a digitar o nome/UF e selecione uma opção da lista."
        )

    def clean(self):
        cleaned_data = super().clean()

        def _apenas_digitos(v):
            if v in (None, "", []):
                return ""
            s = str(v).strip()
            return "".join(ch for ch in s if ch.isdigit())

        def _max_digitos(s, max_len):
            d = _apenas_digitos(s)
            return d[:max_len] if d and max_len and len(d) > max_len else d

        TRIM_DIGIT_FIELDS = [
            ("sind_cep", 8),
            ("sind_ddd1", 4),
            ("sind_ddd2", 4),
            ("sind_fone1", 20),
            ("sind_fone2", 20),
            ("sind_cnpj", 14),
            ("sind_codi_sind", 15),
            ("sind_codi_cede", 15),
        ]
        for campo, max_len in TRIM_DIGIT_FIELDS:
            if campo in cleaned_data:
                val = _max_digitos(cleaned_data.get(campo), max_len)
                cleaned_data[campo] = val or None

        def _to_int_or_none(v):
            if v in (None, "", [], ()):
                return None
            if isinstance(v, int):
                return v
            s = str(v).strip()
            if not s:
                return None
            if s.lstrip("-").isdigit():
                try:
                    return int(s)
                except (TypeError, ValueError):
                    return None
            return None

        def _to_decimal_or_none(v):
            if v in (None, "", [], ()):
                return None
            if isinstance(v, (int, float)):
                return v
            s = str(v).strip().replace(",", ".")
            if not s:
                return None
            try:
                parts = s.split(".")
                if len(parts) == 2 and parts[0].lstrip("-").isdigit() and parts[1].isdigit():
                    pass
                elif s.lstrip("-").isdigit():
                    pass
                else:
                    return None
                from decimal import Decimal
                return Decimal(s)
            except (TypeError, ValueError):
                return None

        ALL_INTEGER_FIELDS = [
            "sind_tipo_entidade",
            "sind_agencia_grcs",
            "sind_logr",
            "sind_tabela",
        ]
        for campo in ALL_INTEGER_FIELDS:
            if campo in cleaned_data:
                cleaned_data[campo] = _to_int_or_none(cleaned_data.get(campo))

        ALL_DECIMAL_FIELDS = [
        ]
        for campo in ALL_DECIMAL_FIELDS:
            if campo in cleaned_data:
                cleaned_data[campo] = _to_decimal_or_none(cleaned_data.get(campo))

        cleaned_data["sind_cida_codi"] = _to_int_or_none(cleaned_data.get("sind_cida_codi"))

        return cleaned_data
