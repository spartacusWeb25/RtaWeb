import re
from django import forms
from django.core.validators import MaxLengthValidator, EmailValidator
from django.db import models as db_models

from sindicatos.models import Sindicatos
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


def _choices_with_current_eventos(choices_tuple, current_value):
    if current_value is None or current_value == "":
        return choices_tuple
    valores_atuais = set()
    for item in choices_tuple:
        if isinstance(item, (list, tuple)) and len(item) >= 1:
            valores_atuais.add(str(item[0]))
    atual = str(current_value)
    if atual in valores_atuais:
        return choices_tuple
    try:
        current_int = int(current_value)
        extra = [(current_int, "{} — {}".format(current_int, current_int))]
    except (TypeError, ValueError):
        extra = [(str(current_value), "{} — {}".format(current_value, current_value))]
    out = list(choices_tuple)
    out.extend(extra)
    return tuple(out)


def _sanitize_choices_for_select(choices):
    if choices is None:
        return (("", "Selecione"),)
    try:
        flat = list(choices)
    except TypeError:
        return (("", "Selecione"),)
    limpa = []
    for item in flat:
        if item is None:
            continue
        if isinstance(item, (list, tuple)):
            if len(item) >= 2:
                try:
                    k = item[0]
                    v = item[1]
                except Exception:
                    continue
                if isinstance(k, bool) or isinstance(v, bool):
                    continue
                limpa.append((k, v))
    return tuple(limpa)


SINDICATOS_VERBAS_EVENTOS_PARES = (
    ("sind_dv_verba_multa_codi", "sind_dv_verba_multa_desc"),
)


TIPO_ENTIDADE_CHOICES = (
    ("", "Selecione"),
    (1, "Sindicato"),
    (2, "Associação"),
    (3, "Federação"),
    (4, "Confederação"),
    (5, "Outros"),
)

LIMINAR_AVISO_CHOICES = (
    ("", "Selecione"),
    (1, "Possui"),
    (2, "Não possui"),
)

MAIORES_MESES_MEDIA_CHOICES = (
    ("", "Selecione"),
    (1, "Proporcionalizar média"),
)

MEDIA_FERIAS_CHOICES = (
    ("", "Selecione"),
    (1, "R. V. últimos meses trab. - H.E. período aquisitivo"),
)

MEDIA_ULTIMOS_MESES_CHOICES = (
    ("", "Selecione"),
    (1, "Férias proporcionais dos últimos meses"),
)


COMBO_CHOICES_FIELDS = {
    "sind_logr": TIPO_LOGRADOURO_CHOICES,
    "sind_esta": UF_CHOICES,
    "sind_tipo_entidade": TIPO_ENTIDADE_CHOICES,
    "sind_dv_liminar_aviso_codi": LIMINAR_AVISO_CHOICES,
    "sind_md_maiores_meses_opcao": MAIORES_MESES_MEDIA_CHOICES,
    "sind_md_media_ferias_codi": MEDIA_FERIAS_CHOICES,
    "sind_md_media_ultimos_codi": MEDIA_ULTIMOS_MESES_CHOICES,
}


FIELD_LABELS = {
    "registro": "Registro",
    "sind_empr": "Empresa",
    "sind_fili": "Filial",
    "sind_codi": "Código",
    "sind_nome": "Sindicato",
    "sind_apelido": "Apelido",
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

    # ================================================================
    # ABA 2: DADOS VARIÁVEIS MÊS A MÊS (26)
    # ================================================================
    "sind_dv_piso_salarial": "Piso salarial",
    "sind_dv_base_adicionais": "Base adicionais",
    "sind_dv_indice": "Índice",
    "sind_dv_maior_remuneracao": "Maior remuneração",
    "sind_dv_maior_rem_agrupada": "Considerar maior remuneração sobre verba agrupada",
    "sind_dv_aviso_previo_2anos": "Aviso prévio proporcional a partir de 2 anos",
    "sind_dv_perc_abono_ferias": "% de abono de férias",
    "sind_dv_abono_sigla": "Sigla abono",
    "sind_dv_meses_ferias_dobro": "Quantidade meses para férias dobro",
    "sind_dv_meses_ferias_justa": "Meses para férias em justa causa",
    "sind_dv_ferias_rescisao": "Férias rescisão",
    "sind_dv_perc_adicional_noturno": "% Adicional noturno",
    "sind_dv_data_base_mes": "Data base (mês)",
    "sind_dv_estabilidade_dias": "Estabilidade (dias)",
    "sind_dv_liminar_aviso_codi": "Liminar sobre aviso prévio",
    "sind_dv_liminar_aviso_13": "Aplicar liminar do aviso prévio para 13º indenizado",
    "sind_dv_verba_multa_codi": "Verba multa rescisória (cód.)",
    "sind_dv_verba_multa_desc": "Verba multa rescisória",
    "sind_dv_mes_desc_sindical": "Mês desconto contribuição sindical",
    "sind_dv_meses_homologacao": "Meses para homologação",
    "sind_dv_mes_contribuicao_opcao": "Mês contribuição sindical",
    "sind_dv_hora_noturna_inicio": "Hora noturna início",
    "sind_dv_hora_noturna_fim": "Hora noturna fim",
    "sind_dv_pagar_13_integral_bem": "Pagar 13º salário integral (BEm)",
    "sind_dv_nao_prorroga_aquisitivo_bem": "Não prorroga período aquisitivo (BEm)",

    # ================================================================
    # ABA 3: MÉDIAS (49)
    # ================================================================
    "sind_md_calc_maiores_meses_verba": "Calcular maiores meses de média por verba",
    "sind_md_calc_proporcional_verba": "Calcular proporcionalidade de média por verba",

    # Situação (18 cols)
    "sind_md_sit_rv_mes1": "Meses RV (sit)",
    "sind_md_sit_rv_mes2": "Meses RV (sit)",
    "sind_md_sit_rv_val1": "Rend. Variáveis (sit)",
    "sind_md_sit_rv_val2": "Rend. Variáveis (sit)",
    "sind_md_sit_rv_val3": "Rend. Variáveis (sit)",
    "sind_md_sit_rv_val4": "Rend. Variáveis (sit)",

    "sind_md_sit_he_mes1": "Meses HE (sit)",
    "sind_md_sit_he_mes2": "Meses HE (sit)",
    "sind_md_sit_he_val1": "Horas extras (sit)",
    "sind_md_sit_he_val2": "Horas extras (sit)",
    "sind_md_sit_he_val3": "Horas extras (sit)",
    "sind_md_sit_he_val4": "Horas extras (sit)",

    "sind_md_sit_hn_mes1": "Meses HN (sit)",
    "sind_md_sit_hn_mes2": "Meses HN (sit)",
    "sind_md_sit_hn_val1": "Horas normais (sit)",
    "sind_md_sit_hn_val2": "Horas normais (sit)",
    "sind_md_sit_hn_val3": "Horas normais (sit)",
    "sind_md_sit_hn_val4": "Horas normais (sit)",

    # Férias + 13º (20 cols)
    "sind_md_fer_rv_mes1": "Meses RV (férias)",
    "sind_md_fer_rv_mes2": "Meses RV (férias)",
    "sind_md_fer_rv_val1": "Rend. Variáveis (férias)",
    "sind_md_fer_rv_val2": "Rend. Variáveis (férias)",
    "sind_md_fer_rv_val3": "Rend. Variáveis (férias)",
    "sind_md_fer_rv_val4": "Rend. Variáveis (férias)",

    "sind_md_fer_he_mes1": "Meses HE (férias)",
    "sind_md_fer_he_mes2": "Meses HE (férias)",
    "sind_md_fer_he_val1": "Horas extras (férias)",
    "sind_md_fer_he_val2": "Horas extras (férias)",
    "sind_md_fer_he_val3": "Horas extras (férias)",
    "sind_md_fer_he_val4": "Horas extras (férias)",

    "sind_md_fer_hn_mes1": "Meses HN (férias)",
    "sind_md_fer_hn_mes2": "Meses HN (férias)",
    "sind_md_fer_hn_val1": "Horas normais (férias)",
    "sind_md_fer_hn_val2": "Horas normais (férias)",
    "sind_md_fer_hn_val3": "Horas normais (férias)",
    "sind_md_fer_hn_val4": "Horas normais (férias)",

    "sind_md_fer_calc13_anterior": "Calcular médias 13º sobre exercício anterior",
    "sind_md_fer_calc_112_indeniz": "Calcular 1/12 avos de férias e 13º indenizados sobre as médias indenizadas ",

    # Ignorar meses zerados (3)
    "sind_md_ign_rv": "Ignorar meses zerados (RV)",
    "sind_md_ign_he": "Ignorar meses zerados (HE)",
    "sind_md_ign_hn": "Ignorar meses zerados (HN)",

    # Selects inferiores + checkbox (7)
    "sind_md_maiores_meses_opcao": "Maiores meses para médias",
    "sind_md_maiores_meses_desc": "Maiores meses para médias",
    "sind_md_media_ferias_codi": "Média de férias",
    "sind_md_media_ferias_desc": "Média de férias",
    "sind_md_media_ultimos_codi": "Média últimos meses",
    "sind_md_media_ultimos_desc": "Média últimos meses",
    "sind_md_incluir_mes_atual": "Incluir mês atual para cálculo de médias",
}


class SindicatosTrabalhadoresForm(forms.ModelForm):

    class Meta:
        model = Sindicatos
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

    def _configure_eventos_combos(self):
        from eventos.models import Eventos as _EventosModel

        banco = (
            (getattr(self, "banco", None) or "").strip()
            or (self.initial.get("registro") or "").strip()
            or (getattr(self.instance, "registro", None) or "").strip()
        )
        db_alias = getattr(self, "db_alias", None) or "default"
        empr_contexto = (
            self.initial.get("sind_empr")
            or getattr(self.instance, "sind_empr", None)
        )
        try:
            empr_contexto_int = int(empr_contexto) if empr_contexto not in (None, "") else None
        except (TypeError, ValueError):
            empr_contexto_int = None

        eventos_lista = []
        mapa_even = {}
        if banco:
            try:
                qs = _EventosModel.objects.using(db_alias).filter(
                    registro=banco,
                    even_inativo=False,
                )
                if empr_contexto_int is not None:
                    qs = qs.filter(even_empr=empr_contexto_int)
                qs = qs.order_by("even_codi")
                eventos_lista = list(qs.values("even_codi", "even_desc"))
                for ev in eventos_lista:
                    try:
                        mapa_even[int(ev["even_codi"])] = (ev.get("even_desc") or "").strip()
                    except (TypeError, ValueError):
                        continue
            except Exception:
                eventos_lista = []
                mapa_even = {}

        choices_base = (("", "Selecione"),)
        if eventos_lista:
            _temp_choices = [("", "Selecione")]
            for ev in eventos_lista:
                try:
                    codigo_int = int(ev["even_codi"])
                    descricao = (ev.get("even_desc") or "").strip() or "Sem descrição"
                    _temp_choices.append((codigo_int, "{} — {}".format(codigo_int, descricao)))
                except Exception:
                    continue
            choices_base = tuple(_temp_choices)
        choices_base = _sanitize_choices_for_select(choices_base)
        self._eventos_mapa = mapa_even

        for codigo_field, desc_field in SINDICATOS_VERBAS_EVENTOS_PARES:
            if codigo_field not in self.fields:
                continue
            codigo_atual = self.initial.get(codigo_field)
            if codigo_atual in (None, ""):
                codigo_atual = getattr(self.instance, codigo_field, None)
            try:
                codigo_atual_int = int(codigo_atual) if codigo_atual not in (None, "") else None
            except (TypeError, ValueError):
                codigo_atual_int = None

            choices = _choices_with_current_eventos(choices_base, codigo_atual_int)
            choices = _sanitize_choices_for_select(choices)

            self.fields[codigo_field].required = False
            self.fields[codigo_field].choices = choices
            self.fields[codigo_field].widget = forms.Select(
                choices=choices,
                attrs={"class": "form-select"},
            )

            descricao_automatica = ""
            if codigo_atual_int is not None:
                descricao_automatica = mapa_even.get(codigo_atual_int, "")
                if not descricao_automatica and desc_field in self.fields:
                    descricao_automatica = (
                        (self.initial.get(desc_field) or "").strip()
                        or (getattr(self.instance, desc_field, None) or "").strip()
                    )

            if desc_field in self.fields:
                self.initial[desc_field] = descricao_automatica
                self.fields[desc_field].initial = descricao_automatica
                self.fields[desc_field].required = False

    def clean(self):
        cleaned_data = super().clean() or {}
        mapa_even = getattr(self, "_eventos_mapa", None)
        if not mapa_even:
            try:
                from eventos.models import Eventos as _EventosModel

                banco = (
                    (getattr(self, "banco", None) or "").strip()
                    or (cleaned_data.get("registro") or "").strip()
                    or (getattr(self.instance, "registro", None) or "").strip()
                )
                db_alias = getattr(self, "db_alias", None) or "default"
                empr_contexto = cleaned_data.get("sind_empr") or getattr(self.instance, "sind_empr", None)
                if banco:
                    qs = _EventosModel.objects.using(db_alias).filter(registro=banco)
                    try:
                        qs = qs.filter(even_empr=int(empr_contexto))
                    except (TypeError, ValueError):
                        pass
                    mapa_even = {}
                    for ev in qs.values("even_codi", "even_desc"):
                        try:
                            mapa_even[int(ev["even_codi"])] = (ev.get("even_desc") or "").strip() or ""
                        except (TypeError, ValueError):
                            continue
            except Exception:
                mapa_even = {}

        if mapa_even:
            for codigo_field, desc_field in SINDICATOS_VERBAS_EVENTOS_PARES:
                if desc_field not in self.fields:
                    continue
                cod = cleaned_data.get(codigo_field)
                if cod in (None, ""):
                    cleaned_data[desc_field] = ""
                    continue
                try:
                    cod_int = int(cod)
                except (TypeError, ValueError):
                    cleaned_data[desc_field] = ""
                    continue
                cleaned_data[desc_field] = mapa_even.get(cod_int, "")
        return cleaned_data

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
                        "Ja existe um sindicato trabalhador com este codigo e filial nesta licenca.",
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
            # Dados variáveis (SmallInt / Integer)
            "sind_dv_meses_ferias_dobro",
            "sind_dv_meses_ferias_justa",
            "sind_dv_ferias_rescisao",
            "sind_dv_data_base_mes",
            "sind_dv_estabilidade_dias",
            "sind_dv_liminar_aviso_codi",
            "sind_dv_verba_multa_codi",
            "sind_dv_mes_desc_sindical",
            "sind_dv_meses_homologacao",
            "sind_dv_mes_contribuicao_opcao",
            # Médias (SmallInt / Integer)
            "sind_md_sit_rv_mes1", "sind_md_sit_rv_mes2",
            "sind_md_sit_he_mes1", "sind_md_sit_he_mes2",
            "sind_md_sit_hn_mes1", "sind_md_sit_hn_mes2",
            "sind_md_fer_rv_mes1", "sind_md_fer_rv_mes2",
            "sind_md_fer_he_mes1", "sind_md_fer_he_mes2",
            "sind_md_fer_hn_mes1", "sind_md_fer_hn_mes2",
            "sind_md_maiores_meses_opcao",
            "sind_md_media_ferias_codi",
            "sind_md_media_ultimos_codi",
        ]
        self._DECIMAL_SAFE_FIELDS = [
            "sind_dv_piso_salarial",
            "sind_dv_base_adicionais",
            "sind_dv_indice",
            "sind_dv_maior_remuneracao",
            "sind_dv_perc_abono_ferias",
            "sind_dv_perc_adicional_noturno",
            # Médias: situação
            "sind_md_sit_rv_val1", "sind_md_sit_rv_val2", "sind_md_sit_rv_val3", "sind_md_sit_rv_val4",
            "sind_md_sit_he_val1", "sind_md_sit_he_val2", "sind_md_sit_he_val3", "sind_md_sit_he_val4",
            "sind_md_sit_hn_val1", "sind_md_sit_hn_val2", "sind_md_sit_hn_val3", "sind_md_sit_hn_val4",
            # Médias: férias + 13
            "sind_md_fer_rv_val1", "sind_md_fer_rv_val2", "sind_md_fer_rv_val3", "sind_md_fer_rv_val4",
            "sind_md_fer_he_val1", "sind_md_fer_he_val2", "sind_md_fer_he_val3", "sind_md_fer_he_val4",
            "sind_md_fer_hn_val1", "sind_md_fer_hn_val2", "sind_md_fer_hn_val3", "sind_md_fer_hn_val4",
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
            field.widget.attrs["placeholder"] = "Nome do sindicato trabalhador"
            field.widget.attrs["maxlength"] = 200
            field.required = False

        if "sind_apelido" in self.fields:
            field = self.fields["sind_apelido"]
            field.widget.attrs["placeholder"] = "Apelido / Sigla"
            field.widget.attrs["maxlength"] = 100
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

        if "sind_dv_perc_abono_ferias" in self.fields:
            field = self.fields["sind_dv_perc_abono_ferias"]
            field.widget = forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "0,00",
                "inputmode": "decimal",
                "maxlength": "12",
                "data-decimal-only": "true",
            })
            field.required = False

        for fname in ("sind_dv_hora_noturna_inicio", "sind_dv_hora_noturna_fim"):
            if fname in self.fields:
                f = self.fields[fname]
                f.widget = forms.TextInput(attrs={
                    "class": "form-control",
                    "placeholder": "00:00",
                    "inputmode": "numeric",
                    "maxlength": "5",
                    "data-time-hhmm": "true",
                })
                f.max_length = 5
                f.required = False

        if "sind_dv_abono_sigla" in self.fields:
            self.fields["sind_dv_abono_sigla"].widget = forms.HiddenInput()
            self.fields["sind_dv_abono_sigla"].required = False

        self._configure_eventos_combos()

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
        match_codigo = re.search(r"\d{6,}", valor_str)
        if match_codigo:
            try:
                return int(match_codigo.group(0))
            except (TypeError, ValueError):
                return None
        apenas_digitos = "".join(ch for ch in valor_str if ch.isdigit())
        if apenas_digitos:
            try:
                return int(apenas_digitos)
            except (TypeError, ValueError):
                return None
        return None

    def clean_sind_dv_perc_abono_ferias(self):
        valor = (self.cleaned_data.get("sind_dv_perc_abono_ferias") or "").strip()
        if not valor:
            return None
        valor_limpo = valor.replace(".", "").replace(",", ".")
        apenas_permitidos = all(ch.isdigit() or ch == "." for ch in valor_limpo)
        if not apenas_permitidos:
            raise forms.ValidationError("Informe um valor numérico válido.")
        try:
            return float(valor_limpo)
        except (TypeError, ValueError):
            raise forms.ValidationError("Informe um valor numérico válido (ex: 33,33).")

    def clean_sind_dv_perc_adicional_noturno(self):
        valor = (self.cleaned_data.get("sind_dv_perc_adicional_noturno") or "").strip()
        if not valor:
            return None
        valor_limpo = str(valor).replace(".", "").replace(",", ".")
        apenas_permitidos = all(ch.isdigit() or ch == "." for ch in valor_limpo)
        if not apenas_permitidos:
            raise forms.ValidationError("Informe um valor numérico válido.")
        try:
            return float(valor_limpo)
        except (TypeError, ValueError):
            raise forms.ValidationError("Informe um valor numérico válido.")

    @staticmethod
    def _clean_hora_hhmm(valor):
        valor = (valor or "").strip()
        if not valor:
            return None
        apenas_digitos = "".join(ch for ch in valor if ch.isdigit())
        if len(apenas_digitos) < 3:
            raise forms.ValidationError("Informe uma hora válida no formato 00:00.")
        if len(apenas_digitos) == 3:
            apenas_digitos = "0" + apenas_digitos
        apenas_digitos = apenas_digitos[:4]
        hh = int(apenas_digitos[:2])
        mm = int(apenas_digitos[2:4])
        if hh > 23:
            raise forms.ValidationError("Hora deve estar entre 00 e 23.")
        if mm > 59:
            raise forms.ValidationError("Minutos devem estar entre 00 e 59.")
        return "{:02d}:{:02d}".format(hh, mm)

    def clean_sind_dv_hora_noturna_inicio(self):
        return self._clean_hora_hhmm(self.cleaned_data.get("sind_dv_hora_noturna_inicio"))

    def clean_sind_dv_hora_noturna_fim(self):
        return self._clean_hora_hhmm(self.cleaned_data.get("sind_dv_hora_noturna_fim"))
