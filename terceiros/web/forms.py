import re
from django import forms
from django.core.validators import MaxLengthValidator
from django.db import models as db_models

from terceiros.models import Terceiros
from terceiros.web.choices import (
    TIPO_LOGRADOURO_CHOICES,
    TIPO_SANGUINEO_CHOICES,
    ETNIA_RACA_CHOICES,
    COR_CABELO_CHOICES,
    COR_OLHOS_CHOICES,
    SEXO_CHOICES,
    ESTADO_CIVIL_CHOICES,
    GRAU_INSTRUCAO_CHOICES,
    UF_CHOICES,
    TIPO_CONTA_CHOICES,
    MODO_PAGAMENTO_CHOICES,
    BANCOS_CHOICES,
    CATEGORIA_SEFIP_CHOICES,
    CATEGORIA_ESOCIAL_CHOICES,
    GRAU_RISCO_CHOICES,
    NATUREZA_OCUPACAO_CHOICES,
    TEMPO_RESIDENCIA_CHOICES,
    CONDICAO_INGRESSO_CHOICES,
    COUNTRY_CHOICES,
    CLASSE_TERCEIRO_CHOICES,
    DEFICIENCIA_CHOICES,
    TRIBUTACAO_IRRF_EXTERIOR_CHOICES,
    CIDADES_TOP_BR_CHOICES,
    CIDADES_POR_CODIGO,
    PAISES_POR_CODIGO,
    _choices_with_current,
    _current_field_value,
)


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


COMBO_CHOICES_FIELDS = {
    "terc_logr": TIPO_LOGRADOURO_CHOICES,
    "terc_tipo_sanguineo": TIPO_SANGUINEO_CHOICES,
    "terc_etnia_raca": ETNIA_RACA_CHOICES,
    "terc_cor_cabelo": COR_CABELO_CHOICES,
    "terc_cor_olhos": COR_OLHOS_CHOICES,
    "terc_sexo": SEXO_CHOICES,
    "terc_estado_civil": ESTADO_CIVIL_CHOICES,
    "terc_grau_instrucao": GRAU_INSTRUCAO_CHOICES,
    "terc_ende_uf": UF_CHOICES,
    "terc_uf_rg": UF_CHOICES,
    "terc_ctps_uf": UF_CHOICES,
    "terc_naturalidade": UF_CHOICES,
    "terc_tipo_conta": TIPO_CONTA_CHOICES,
    "terc_modo_pagamento": MODO_PAGAMENTO_CHOICES,
    "terc_categoria_sefip": CATEGORIA_SEFIP_CHOICES,
    "terc_categoria_esocial": CATEGORIA_ESOCIAL_CHOICES,
    "terc_grau_risco": GRAU_RISCO_CHOICES,
    "terc_natureza_ocupacao": NATUREZA_OCUPACAO_CHOICES,
    "terc_tempo_residencia": TEMPO_RESIDENCIA_CHOICES,
    "terc_condicao_ingresso": CONDICAO_INGRESSO_CHOICES,
    "terc_classe": CLASSE_TERCEIRO_CHOICES,
    "terc_tributacao_irrf_exterior": TRIBUTACAO_IRRF_EXTERIOR_CHOICES,
}


FIELD_LABELS = {
    "registro": "Registro",
    "terc_empr": "Empresa",
    "terc_fili": "Filial",
    "terc_codi": "Código",
    "terc_nome": "Nome",
    "terc_inativo": "Inativo",
    "terc_cpf": "CPF",
    "terc_cep": "CEP",
    "terc_logr": "Logradouro",
    "terc_ende": "Endereço",
    "terc_ende_nume": "Número",
    "terc_ende_comp": "Complemento",
    "terc_ende_bair": "Bairro",
    "terc_ende_cida_codi": "Cidade (Código IBGE)",
    "terc_ende_cida_desc": "Cidade",
    "terc_ende_uf": "UF",
    "terc_ddd": "DDD",
    "terc_telefone": "Telefone",
    "terc_ddd_celular": "DDD",
    "terc_celular": "Celular",
    "terc_email": "E-mail",
    "terc_tipo_sanguineo": "Tipo sanguíneo",
    "terc_etnia_raca": "Etnia / Raça",
    "terc_cor_cabelo": "Cor do cabelo",
    "terc_cor_olhos": "Cor dos olhos",
    "terc_pessoa_com_deficiencia": "Pessoa com deficiência",
    "terc_observacoes_deficiencias": "Observação deficiência",
    "terc_altura_metros": "Altura (m)",
    "terc_peso_kg": "Peso (kg)",
    "terc_sinais_no_corpo": "Sinais no corpo",
    "terc_nascimento": "Data de nascimento",
    "terc_cidade_nascimento_codi": "Cidade de nascimento (código)",
    "terc_cidade_nascimento_desc": "Cidade de nascimento",
    "terc_naturalidade": "Naturalidade (UF)",
    "terc_nome_mae": "Nome da mãe",
    "terc_grau_instrucao": "Grau de instrução",
    "terc_sexo": "Sexo",
    "terc_estado_civil": "Estado civil",
    "terc_controlar_manual_dependentes_ir": "Controlar manualmente dependentes IR",
    "terc_numero_dependentes_ir": "Número de dependentes IR",
    "terc_pais_nacionalidade_codi": "País nacionalidade (código)",
    "terc_pais_nacionalidade_desc": "País nacionalidade",
    "terc_chegada_brasil": "Data de chegada ao Brasil",
    "terc_casado_brasileiro": "Casado(a) com brasileiro(a)",
    "terc_tem_filhos_brasileiros": "Tem filhos brasileiros",
    "terc_rne": "RNE",
    "terc_orgao_uf_emissao_rne": "Órgão e UF emissor RNE",
    "terc_emissao_rne": "Data emissão RNE",
    "terc_tempo_residencia": "Tempo de residência",
    "terc_condicao_ingresso": "Condição de ingresso",
    "terc_pais_residencia_codi": "País de residência (código)",
    "terc_pais_residencia_desc": "País de residência",
    "terc_residencia_exterior": "Residência no exterior",
    "terc_ende_exterior": "Endereço",
    "terc_ende_exterior_nume": "Número",
    "terc_ende_exterior_comp": "Complemento",
    "terc_ende_exterior_bair": "Bairro",
    "terc_ende_exterior_cidade": "Cidade",
    "terc_ende_exterior_codigo_postal": "CEP/Código postal",
    "terc_banco": "Banco",
    "terc_banco_desc": "Banco (descrição)",
    "terc_conta_corrente": "Conta corrente",
    "terc_digito_conta_corrente": "Dígito",
    "terc_tipo_conta": "Tipo de conta",
    "terc_modo_pagamento": "Modo de pagamento",
    "terc_rg": "RG",
    "terc_orgao_emissor_rg": "Órgão emissor",
    "terc_emissao_rg": "Data de emissão",
    "terc_uf_rg": "UF",
    "terc_certificado_reservista": "Certificado de reservista",
    "terc_titulo_eleitor": "Título de eleitor",
    "terc_zona_titulo": "Zona eleitoral",
    "terc_secao_titulo": "Seção eleitoral",
    "terc_conselho_regional_numero": "Nº conselho regional",
    "terc_conselho_regional_sigla": "Sigla conselho",
    "terc_ctps_numero": "Carteira de trabalho/CTPS",
    "terc_ctps_serie": "Série",
    "terc_ctps_digito": "Dígito série",
    "terc_ctps_data": "Data de emissão",
    "terc_ctps_uf": "UF",
    "terc_carne_inss_numero": "Nº inscrição carne INSS",
    "terc_codigo_ccm": "Código CCM",
    "terc_carteira_identidade_arquivo": "Carteira de identidade (arquivo)",
    "terc_classe": "Classe",
    "terc_classe_desc": "Classe (descrição)",
    "terc_cbo": "CBO",
    "terc_cbo_desc": "CBO (descrição)",
    "terc_natureza_ocupacao": "Natureza de ocupação",
    "terc_categoria_sefip": "Categoria Sefip",
    "terc_categoria_esocial": "Categoria eSocial",
    "terc_grau_risco": "Grau de risco",
    "terc_transportador_autonomo_perc_inss": "Transportador autônomo % contrib. INSS",
    "terc_percentual_contr_ir": "% contribuição IR",
    "terc_descontar_iss": "Descontar ISS",
    "terc_percentual_iss": "% ISS",
    "terc_tributacao_irrf_exterior": "Tributação IRRF exterior",
    "terc_tributacao_irrf_exterior_desc": "Tributação IRRF exterior (descrição)",
    "terc_rat_aposentadoria_perc": "RAT aposentadoria (%)",
    "terc_acordo_internacional_inss": "Acordo internacional INSS",
    "terc_percentual_irrf_exterior": "% IRRF exterior",
    "terc_nif": "NIF",
    "terc_beneficiario_dispensado_nif": "Beneficiário dispensado NIF",
    "terc_pais_nao_exige_nif": "País não exige NIF",
    "terc_cartao_ponto": "Cartão ponto",
    "terc_data_admissao": "Data de admissão",
}


class TerceirosForm(forms.ModelForm):

    terc_carteira_identidade_arquivo = forms.FileField(
        required=False,
        label="Upload Carteira de Identidade",
        widget=forms.ClearableFileInput(attrs={"accept": "image/*", "class": "form-control"}),
    )

    class Meta:
        model = Terceiros
        fields = "__all__"
        labels = FIELD_LABELS

    _NUMERIC_SAFE_FIELDS = None
    _DECIMAL_SAFE_FIELDS = None

    def validate_unique(self):
        exclude = ["registro", "terc_empr", "terc_fili", "terc_codi"]
        try:
            super().validate_unique(exclude=exclude)
        except Exception:
            pass
        cleaned = getattr(self, "cleaned_data", None) or {}
        reg = (cleaned.get("registro") or "").strip()
        emp = cleaned.get("terc_empr")
        fil = cleaned.get("terc_fili")
        cod = cleaned.get("terc_codi")
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
                        terc_empr=int(emp),
                        terc_fili=int(fil),
                        terc_codi=int(cod),
                    )
                )
                if self.instance.pk is not None:
                    try:
                        qs = qs.exclude(pk=self.instance.pk)
                    except Exception:
                        pass
                if qs.exists():
                    self.add_error(
                        "terc_codi",
                        "Ja existe um terceiro com este codigo e filial nesta licenca.",
                    )
            except Exception:
                pass

    def _init_safe_field_lists(self):
        self._NUMERIC_SAFE_FIELDS = [
            "terc_logr",
            "terc_etnia_raca",
            "terc_cor_cabelo",
            "terc_cor_olhos",
            "terc_grau_instrucao",
            "terc_sexo",
            "terc_estado_civil",
            "terc_numero_dependentes_ir",
            "terc_tempo_residencia",
            "terc_condicao_ingresso",
            "terc_banco",
            "terc_tipo_conta",
            "terc_modo_pagamento",
            "terc_classe",
            "terc_natureza_ocupacao",
            "terc_categoria_sefip",
            "terc_categoria_esocial",
            "terc_grau_risco",
            "terc_tributacao_irrf_exterior",
            "terc_cartao_ponto",
            "terc_ende_cida_codi",
            "terc_cidade_nascimento_codi",
            "terc_pais_nacionalidade_codi",
            "terc_pais_residencia_codi",
        ]
        self._DECIMAL_SAFE_FIELDS = [
            "terc_altura_metros",
            "terc_peso_kg",
            "terc_transportador_autonomo_perc_inss",
            "terc_percentual_contr_ir",
            "terc_percentual_iss",
            "terc_rat_aposentadoria_perc",
            "terc_percentual_irrf_exterior",
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
        self.empr_codigo = kwargs.pop("empr_codigo", None)
        self.fili_codigo = kwargs.pop("fili_codigo", None)
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

        if "registro" in self.fields:
            self.fields["registro"].widget = forms.HiddenInput()
            self.fields["registro"].required = False

        if "terc_empr" in self.fields:
            self.fields["terc_empr"].required = True
            self.fields["terc_empr"].label = "Empresa"
            self.fields["terc_empr"].widget.attrs["readonly"] = "readonly"

        if "terc_fili" in self.fields:
            self.fields["terc_fili"].required = True
            self.fields["terc_fili"].label = "Filial"
            self.fields["terc_fili"].widget.attrs["readonly"] = "readonly"

        for desc_field in (
            "terc_pais_nacionalidade_desc",
            "terc_pais_residencia_desc",
            "terc_banco_desc",
            "terc_classe_desc",
            "terc_cbo_desc",
            "terc_tributacao_irrf_exterior_desc",
        ):
            if desc_field in self.fields:
                self.fields[desc_field].widget = forms.HiddenInput()
                self.fields[desc_field].required = False
                self.fields[desc_field].validators = [
                    v for v in self.fields[desc_field].validators
                    if not isinstance(v, MaxLengthValidator)
                ]

        if "terc_cidade_nascimento_desc" in self.fields:
            field = self.fields["terc_cidade_nascimento_desc"]
            field.widget = forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 60,
                "placeholder": "Nome da cidade de nascimento preenchido automaticamente, editável",
            })
            field.label = "Cidade de nascimento"
            field.required = False

        if "terc_ende_cida_desc" in self.fields:
            field = self.fields["terc_ende_cida_desc"]
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

        if "terc_cpf" in self.fields:
            field = self.fields["terc_cpf"]
            field.max_length = 14
            field.widget.attrs["maxlength"] = 14
            field.widget.attrs["data-mask"] = "cpf"
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["placeholder"] = "000.000.000-00"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "terc_cep" in self.fields:
            field = self.fields["terc_cep"]
            field.max_length = 9
            field.widget.attrs["maxlength"] = 9
            field.widget.attrs["data-mask"] = "cep"
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["placeholder"] = "00000-000"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "terc_rg" in self.fields:
            field = self.fields["terc_rg"]
            field.widget.attrs["data-mask"] = "rg"
            field.widget.attrs["inputmode"] = "numeric"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "terc_ctps_numero" in self.fields:
            field = self.fields["terc_ctps_numero"]
            field.max_length = 20
            field.widget.attrs["maxlength"] = 20
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "terc_ctps_serie" in self.fields:
            field = self.fields["terc_ctps_serie"]
            field.max_length = 10
            field.widget.attrs["maxlength"] = 10
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "terc_ctps_digito" in self.fields:
            field = self.fields["terc_ctps_digito"]
            field.max_length = 2
            field.widget.attrs["maxlength"] = 2
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "terc_ctps_uf" in self.fields:
            field = self.fields["terc_ctps_uf"]
            field.widget.attrs["style"] = ""
            field.required = False

        if "terc_titulo_eleitor" in self.fields:
            field = self.fields["terc_titulo_eleitor"]
            field.max_length = 20
            field.widget.attrs["maxlength"] = 20
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "terc_zona_titulo" in self.fields:
            field = self.fields["terc_zona_titulo"]
            field.max_length = 5
            field.widget.attrs["maxlength"] = 5
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "terc_secao_titulo" in self.fields:
            field = self.fields["terc_secao_titulo"]
            field.max_length = 5
            field.widget.attrs["maxlength"] = 5
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "terc_certificado_reservista" in self.fields:
            field = self.fields["terc_certificado_reservista"]
            field.max_length = 30
            field.widget.attrs["maxlength"] = 30
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "terc_rne" in self.fields:
            field = self.fields["terc_rne"]
            field.max_length = 20
            field.widget.attrs["maxlength"] = 20
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "terc_cbo" in self.fields:
            try:
                from cargos.services.logic import CargosService as _CS_TERC_CBO
                from cargos.services.logic import _digits_only as _digits_only_terc_cbo_nat

                _banco_terc_cbo = self.banco or getattr(getattr(self, "instance", None), "registro", None) or ""
                _banco_terc_cbo_clean = _digits_only_terc_cbo_nat(_banco_terc_cbo) if _banco_terc_cbo else ""
                _valor_atual_cbo_terc = _current_field_value(self, "terc_cbo")
                if _banco_terc_cbo_clean:
                    _cbo_choices_nacional = _CS_TERC_CBO.choices_cbos(
                        banco=_banco_terc_cbo_clean,
                        db_alias=self.db_alias,
                        incluir_selecione=True,
                        valor_atual=_valor_atual_cbo_terc,
                    )
                else:
                    _cbo_choices_nacional = [(None, "Selecione")]
                    try:
                        _val_c_terc = "".join(ch for ch in str(_valor_atual_cbo_terc or "") if ch.isdigit())[:6]
                        if _val_c_terc:
                            _cbo_choices_nacional.append((_val_c_terc, f"{_val_c_terc} - CBO {_val_c_terc} (atual)"))
                    except Exception:
                        pass
                self.fields["terc_cbo"].label = "CBO"
                self.fields["terc_cbo"].widget = forms.Select(
                    attrs={"class": "form-select"},
                    choices=list(_cbo_choices_nacional),
                )
                self.fields["terc_cbo"].required = False
                self.fields["terc_cbo"].validators = [
                    v for v in self.fields["terc_cbo"].validators
                    if not isinstance(v, MaxLengthValidator)
                ]
            except Exception:
                valor_atual = _current_field_value(self, "terc_cbo")
                self.fields["terc_cbo"].label = "CBO"
                self.fields["terc_cbo"].widget = forms.Select(
                    attrs={"class": "form-select"},
                    choices=_choices_with_current((("", "Selecione"),), valor_atual),
                )
                self.fields["terc_cbo"].required = False

        if "terc_ddd" in self.fields:
            field = self.fields["terc_ddd"]
            field.max_length = 2
            field.widget.attrs["maxlength"] = 2
            field.widget.attrs["data-mask"] = "ddd"
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["placeholder"] = "00"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "terc_ddd_celular" in self.fields:
            field = self.fields["terc_ddd_celular"]
            field.max_length = 2
            field.widget.attrs["maxlength"] = 2
            field.widget.attrs["data-mask"] = "ddd"
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["placeholder"] = "00"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "terc_telefone" in self.fields:
            field = self.fields["terc_telefone"]
            field.max_length = 9
            field.widget.attrs["maxlength"] = 9
            field.widget.attrs["data-mask"] = "telefone"
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["placeholder"] = "0000-0000"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "terc_celular" in self.fields:
            field = self.fields["terc_celular"]
            field.max_length = 11
            field.widget.attrs["maxlength"] = 15
            field.widget.attrs["data-mask"] = "celular"
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["placeholder"] = "00000-0000"
            field.validators = [v for v in field.validators if not isinstance(v, MaxLengthValidator)]
            field.required = False

        if "terc_email" in self.fields:
            field = self.fields["terc_email"]
            field.widget.attrs["placeholder"] = "exemplo@email.com"
            field.widget.attrs["type"] = "email"
            field.required = False

        if "terc_carne_inss_numero" in self.fields:
            field = self.fields["terc_carne_inss_numero"]
            field.max_length = 20
            field.widget.attrs["maxlength"] = 20
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "terc_conta_corrente" in self.fields:
            field = self.fields["terc_conta_corrente"]
            field.max_length = 20
            field.widget.attrs["maxlength"] = 20
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "terc_digito_conta_corrente" in self.fields:
            field = self.fields["terc_digito_conta_corrente"]
            field.max_length = 5
            field.widget.attrs["maxlength"] = 5
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "terc_codigo_ccm" in self.fields:
            field = self.fields["terc_codigo_ccm"]
            field.max_length = 20
            field.widget.attrs["maxlength"] = 20
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "terc_nif" in self.fields:
            field = self.fields["terc_nif"]
            field.max_length = 30
            field.widget.attrs["maxlength"] = 30
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "terc_conselho_regional_numero" in self.fields:
            field = self.fields["terc_conselho_regional_numero"]
            field.max_length = 30
            field.widget.attrs["maxlength"] = 30
            field.widget.attrs["inputmode"] = "numeric"
            field.widget.attrs["data-digits-only"] = "true"
            field.required = False

        if "terc_conselho_regional_sigla" in self.fields:
            field = self.fields["terc_conselho_regional_sigla"]
            field.widget.attrs["style"] = "text-transform: uppercase;"
            field.required = False

        if "terc_uf_rg" in self.fields:
            field = self.fields["terc_uf_rg"]
            field.widget.attrs["style"] = ""
            field.required = False

        if "terc_banco" in self.fields:
            field = self.fields["terc_banco"]
            field.required = False
            field.label = "Banco"
            _val = _current_field_value(self, "terc_banco")
            field.widget = forms.Select(
                choices=_choices_with_current(BANCOS_CHOICES, _val),
                attrs={"class": "form-select form-select-md terceiro-select"},
            )

        if "terc_categoria_esocial" in self.fields:
            valor_atual = _current_field_value(self, "terc_categoria_esocial")
            self.fields["terc_categoria_esocial"].label = "Categoria eSocial"
            self.fields["terc_categoria_esocial"].choices = _choices_with_current(
                CATEGORIA_ESOCIAL_CHOICES, valor_atual
            )
            self.fields["terc_categoria_esocial"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(CATEGORIA_ESOCIAL_CHOICES, valor_atual),
            )
            self.fields["terc_categoria_esocial"].required = False

        if "terc_pais_residencia_codi" in self.fields:
            valor_atual = _current_field_value(self, "terc_pais_residencia_codi")
            self.fields["terc_pais_residencia_codi"].label = "País de residência"
            self.fields["terc_pais_residencia_codi"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(COUNTRY_CHOICES, valor_atual),
            )
            self.fields["terc_pais_residencia_codi"].required = False

        if "terc_pais_nacionalidade_codi" in self.fields:
            valor_atual = _current_field_value(self, "terc_pais_nacionalidade_codi")
            self.fields["terc_pais_nacionalidade_codi"].label = "País nacionalidade"
            self.fields["terc_pais_nacionalidade_codi"].widget = forms.Select(
                attrs={"class": "form-select"},
                choices=_choices_with_current(COUNTRY_CHOICES, valor_atual),
            )
            self.fields["terc_pais_nacionalidade_codi"].required = False

        if "terc_residencia_exterior" in self.fields:
            self.fields["terc_residencia_exterior"].widget = forms.HiddenInput()
            self.fields["terc_residencia_exterior"].required = False

        if "terc_ende_cida_codi" in self.fields:
            valor_atual = _current_field_value(self, "terc_ende_cida_codi")
            self.fields["terc_ende_cida_codi"] = forms.CharField(
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
                            self.initial["terc_ende_cida_codi"] = f"{cod_num:07d} — {nome} / {uf}"
                        else:
                            self.initial["terc_ende_cida_codi"] = f"{cod_num:07d} — {cod_num}"
                except (TypeError, ValueError):
                    pass

        if "terc_cidade_nascimento_codi" in self.fields:
            valor_atual = _current_field_value(self, "terc_cidade_nascimento_codi")
            self.fields["terc_cidade_nascimento_codi"] = forms.CharField(
                label="Cidade de nascimento (código)",
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
                            self.initial["terc_cidade_nascimento_codi"] = f"{cod_num:07d} — {nome} / {uf}"
                        else:
                            self.initial["terc_cidade_nascimento_codi"] = f"{cod_num:07d} — {cod_num}"
                except (TypeError, ValueError):
                    pass

    def clean_terc_cpf(self):
        valor = (self.cleaned_data.get("terc_cpf") or "").strip()
        digits = _only_digits(valor)[:11]
        if digits and not _cpf_valido(digits):
            raise forms.ValidationError("Informe um CPF válido.")
        return digits or None

    def clean_terc_cep(self):
        valor = (self.cleaned_data.get("terc_cep") or "").strip()
        digits = _only_digits(valor)[:8]
        if digits and len(digits) != 8:
            raise forms.ValidationError("Informe um CEP válido com 8 dígitos.")
        return digits or None

    def clean_terc_ddd(self):
        return _only_digits(self.cleaned_data.get("terc_ddd"))[:2] or None

    def clean_terc_telefone(self):
        return _only_digits(self.cleaned_data.get("terc_telefone"))[:9] or None

    def clean_terc_ddd_celular(self):
        return _only_digits(self.cleaned_data.get("terc_ddd_celular"))[:2] or None

    def clean_terc_celular(self):
        return _only_digits(self.cleaned_data.get("terc_celular"))[:11] or None

    def clean_terc_rg(self):
        valor = (self.cleaned_data.get("terc_rg") or "").strip()
        return _only_digits(valor)[:20] or None

    def clean_terc_conta_corrente(self):
        valor = (self.cleaned_data.get("terc_conta_corrente") or "").strip()
        return _only_digits(valor)[:20] or None

    def clean_terc_digito_conta_corrente(self):
        valor = (self.cleaned_data.get("terc_digito_conta_corrente") or "").strip()
        return _only_digits(valor)[:5] or None

    def clean_terc_certificado_reservista(self):
        return _only_digits(self.cleaned_data.get("terc_certificado_reservista"))[:30] or None

    def clean_terc_titulo_eleitor(self):
        return _only_digits(self.cleaned_data.get("terc_titulo_eleitor"))[:12] or None

    def clean_terc_zona_titulo(self):
        return _only_digits(self.cleaned_data.get("terc_zona_titulo"))[:4] or None

    def clean_terc_secao_titulo(self):
        return _only_digits(self.cleaned_data.get("terc_secao_titulo"))[:4] or None

    def clean_terc_ctps_numero(self):
        return _only_digits(self.cleaned_data.get("terc_ctps_numero"))[:7] or None

    def clean_terc_ctps_serie(self):
        return _only_digits(self.cleaned_data.get("terc_ctps_serie"))[:4] or None

    def clean_terc_ctps_digito(self):
        return _only_digits(self.cleaned_data.get("terc_ctps_digito"))[:2] or None

    def clean_terc_carne_inss_numero(self):
        return _only_digits(self.cleaned_data.get("terc_carne_inss_numero"))[:20] or None

    def clean_terc_codigo_ccm(self):
        return _only_digits(self.cleaned_data.get("terc_codigo_ccm"))[:20] or None

    def clean_terc_nif(self):
        return _only_digits(self.cleaned_data.get("terc_nif"))[:30] or None

    def clean_terc_conselho_regional_numero(self):
        return _only_digits(self.cleaned_data.get("terc_conselho_regional_numero"))[:30] or None

    def clean_terc_cbo(self):
        return _only_digits(self.cleaned_data.get("terc_cbo"))[:6] or None

    def clean_terc_rne(self):
        return _only_digits(self.cleaned_data.get("terc_rne"))[:20] or None

    def clean_terc_ende_cida_codi(self):
        valor = self.cleaned_data.get("terc_ende_cida_codi")
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
            self.cleaned_data["terc_ende_cida_desc"] = f"{nome} / {uf}"
            return match_codigo
        if match_codigo is not None and 1 <= len(apenas_digitos) <= 7:
            self.cleaned_data["terc_ende_cida_desc"] = str(match_codigo)
            return match_codigo
        texto_busca = valor_str.lower()
        if texto_busca:
            for cod_num, (n, u) in CIDADES_POR_CODIGO.items():
                l1 = f"{cod_num:07d} — {n} / {u}".lower()
                l2 = f"{n} {u}".lower()
                l3 = f"{n}/{u}".lower()
                if (texto_busca in l1) or (texto_busca in l2) or (texto_busca in l3):
                    self.cleaned_data["terc_ende_cida_desc"] = f"{n} / {u}"
                    return cod_num
        raise forms.ValidationError(
            "Cidade não encontrada. Digite o código IBGE de 7 dígitos "
            "ou comece a digitar o nome/UF e selecione uma opção da lista."
        )

    def clean_terc_cidade_nascimento_codi(self):
        valor = self.cleaned_data.get("terc_cidade_nascimento_codi")
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
            self.cleaned_data["terc_cidade_nascimento_desc"] = f"{nome} / {uf}"
            return match_codigo
        if match_codigo is not None and 1 <= len(apenas_digitos) <= 7:
            self.cleaned_data["terc_cidade_nascimento_desc"] = str(match_codigo)
            return match_codigo
        texto_busca = valor_str.lower()
        if texto_busca:
            for cod_num, (n, u) in CIDADES_POR_CODIGO.items():
                l1 = f"{cod_num:07d} — {n} / {u}".lower()
                l2 = f"{n} {u}".lower()
                l3 = f"{n}/{u}".lower()
                if (texto_busca in l1) or (texto_busca in l2) or (texto_busca in l3):
                    self.cleaned_data["terc_cidade_nascimento_desc"] = f"{n} / {u}"
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
            ("terc_cpf", 11),
            ("terc_cep", 8),
            ("terc_ddd", 2),
            ("terc_ddd_celular", 2),
            ("terc_telefone", 9),
            ("terc_celular", 11),
            ("terc_rg", 20),
            ("terc_ctps_numero", 7),
            ("terc_ctps_serie", 4),
            ("terc_ctps_digito", 2),
            ("terc_titulo_eleitor", 12),
            ("terc_zona_titulo", 4),
            ("terc_secao_titulo", 4),
            ("terc_certificado_reservista", 30),
            ("terc_rne", 20),
            ("terc_cbo", 6),
            ("terc_carne_inss_numero", 20),
            ("terc_codigo_ccm", 20),
            ("terc_nif", 30),
            ("terc_conselho_regional_numero", 30),
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
            "terc_logr",
            "terc_etnia_raca",
            "terc_cor_cabelo",
            "terc_cor_olhos",
            "terc_grau_instrucao",
            "terc_sexo",
            "terc_estado_civil",
            "terc_numero_dependentes_ir",
            "terc_tempo_residencia",
            "terc_condicao_ingresso",
            "terc_banco",
            "terc_tipo_conta",
            "terc_modo_pagamento",
            "terc_classe",
            "terc_natureza_ocupacao",
            "terc_categoria_sefip",
            "terc_categoria_esocial",
            "terc_grau_risco",
            "terc_tributacao_irrf_exterior",
            "terc_cartao_ponto",
        ]
        for campo in ALL_INTEGER_FIELDS:
            if campo in cleaned_data:
                cleaned_data[campo] = _to_int_or_none(cleaned_data.get(campo))

        ALL_DECIMAL_FIELDS = [
            "terc_altura_metros",
            "terc_peso_kg",
            "terc_transportador_autonomo_perc_inss",
            "terc_percentual_contr_ir",
            "terc_percentual_iss",
            "terc_rat_aposentadoria_perc",
            "terc_percentual_irrf_exterior",
        ]
        for campo in ALL_DECIMAL_FIELDS:
            if campo in cleaned_data:
                cleaned_data[campo] = _to_decimal_or_none(cleaned_data.get(campo))

        for campo in ("terc_ende_cida_codi", "terc_cidade_nascimento_codi",
                       "terc_pais_nacionalidade_codi", "terc_pais_residencia_codi"):
            cleaned_data[campo] = _to_int_or_none(cleaned_data.get(campo))

        _classe_codi = cleaned_data.get("terc_classe")
        if _classe_codi in (None, ""):
            cleaned_data["terc_classe_desc"] = None
        else:
            try:
                _classe_int = int(_classe_codi)
            except (TypeError, ValueError):
                _classe_int = None
            _classe_desc = ""
            if _classe_int is not None:
                for cod, desc in CLASSE_TERCEIRO_CHOICES:
                    if cod in (None, ""):
                        continue
                    try:
                        if int(cod) == _classe_int:
                            _classe_desc = str(desc)
                            break
                    except (TypeError, ValueError):
                        continue
            if not _classe_desc and _classe_int is not None:
                _classe_desc = f"{_classe_int} - Classe {_classe_int}"
            if _classe_desc:
                _classe_desc = _classe_desc[:120]
            cleaned_data["terc_classe_desc"] = _classe_desc

        _trib_codi = cleaned_data.get("terc_tributacao_irrf_exterior")
        if _trib_codi in (None, ""):
            cleaned_data["terc_tributacao_irrf_exterior_desc"] = None
        else:
            try:
                _trib_int = int(_trib_codi)
            except (TypeError, ValueError):
                _trib_int = None
            _trib_desc = ""
            if _trib_int is not None:
                for cod, desc in TRIBUTACAO_IRRF_EXTERIOR_CHOICES:
                    if cod in (None, ""):
                        continue
                    try:
                        if int(cod) == _trib_int:
                            _trib_desc = str(desc)
                            break
                    except (TypeError, ValueError):
                        continue
            if not _trib_desc and _trib_int is not None:
                _trib_desc = f"{_trib_int} - Tributacao {_trib_int}"
            if _trib_desc:
                _trib_desc = _trib_desc[:80]
            cleaned_data["terc_tributacao_irrf_exterior_desc"] = _trib_desc

        _cbo_codi = cleaned_data.get("terc_cbo")
        if _cbo_codi in (None, "", [], ()):
            cleaned_data["terc_cbo_desc"] = None
        else:
            _cbo_str = str(_cbo_codi).strip()
            if not _cbo_str:
                cleaned_data["terc_cbo_desc"] = None
            else:
                _desc = f"{_cbo_str} - CBO {_cbo_str}"
                if len(_desc) > 160:
                    _desc = _desc[:160]
                cleaned_data["terc_cbo_desc"] = _desc

        _banco_codi = cleaned_data.get("terc_banco")
        if _banco_codi in (None, "", [], ()):
            cleaned_data["terc_banco_desc"] = None
        else:
            _banco_str = str(_banco_codi).strip()
            if not _banco_str:
                cleaned_data["terc_banco_desc"] = None
            else:
                _banco_desc = ""
                for cod, desc in BANCOS_CHOICES:
                    if cod in (None, ""):
                        continue
                    if str(cod).strip() == _banco_str:
                        _banco_desc = str(desc)
                        break
                if not _banco_desc:
                    _banco_desc = f"{_banco_str} - Banco {_banco_str}"
                if len(_banco_desc) > 120:
                    _banco_desc = _banco_desc[:120]
                cleaned_data["terc_banco_desc"] = _banco_desc

        _pais_nac_codi = cleaned_data.get("terc_pais_nacionalidade_codi")
        if _pais_nac_codi in (None, ""):
            cleaned_data["terc_pais_nacionalidade_desc"] = None
        else:
            try:
                _pais_int = int(_pais_nac_codi)
                label = PAISES_POR_CODIGO.get(_pais_int)
                if label:
                    nome = label.split(" - ", 1)[1] if " - " in label else str(label)
                    cleaned_data["terc_pais_nacionalidade_desc"] = nome
                else:
                    cleaned_data["terc_pais_nacionalidade_desc"] = str(_pais_int)
            except (TypeError, ValueError):
                cleaned_data["terc_pais_nacionalidade_desc"] = None

        _pais_res_codi = cleaned_data.get("terc_pais_residencia_codi")
        if _pais_res_codi in (None, ""):
            cleaned_data["terc_pais_residencia_desc"] = None
        else:
            try:
                _pais_int = int(_pais_res_codi)
                label = PAISES_POR_CODIGO.get(_pais_int)
                if label:
                    nome = label.split(" - ", 1)[1] if " - " in label else str(label)
                    cleaned_data["terc_pais_residencia_desc"] = nome
                else:
                    cleaned_data["terc_pais_residencia_desc"] = str(_pais_int)
            except (TypeError, ValueError):
                cleaned_data["terc_pais_residencia_desc"] = None

        return cleaned_data
