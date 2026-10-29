from django.core.exceptions import ValidationError
from django.db import connections
from django.db.models import Q

from empresas.models import Empresas
from eventos.models import Eventos
from eventos_agrupados.models import EventosAgrupados


_TABLE_COLUMNS_CACHE = {}


EVENTO_FIELDS = (
    "even_ferias_proporcionais",
    "even_ferias_vencidas",
    "even_ferias_dobro",
    "even_ferias_indenizadas",
    "even_13_salario",
    "even_13_salario_indenizado",
    "even_aviso_previo_indenizado",
)


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


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


def _get_table_columns(alias: str, table_name: str = "eventos_agrupados") -> set:
    cache_key = (alias or "default", table_name)
    if cache_key in _TABLE_COLUMNS_CACHE:
        return _TABLE_COLUMNS_CACHE[cache_key]
    try:
        with connections[alias or "default"].cursor() as cur:
            cur.execute(
                "SELECT column_name "
                "FROM information_schema.columns "
                "WHERE table_schema = 'public' AND table_name = %s",
                [table_name],
            )
            cols = {row[0] for row in (cur.fetchall() or [])}
    except Exception:
        cols = set()
    _TABLE_COLUMNS_CACHE[cache_key] = cols
    return cols


def _sql_expr(columns: set, column_name: str, default_sql: str) -> str:
    if column_name in columns:
        return column_name
    return f"{default_sql} AS {column_name}"


def _model_default(field):
    internal_type = field.get_internal_type()
    if internal_type in ("CharField", "TextField"):
        return ""
    return None


def _format_evento_label(codigo, descricao):
    codigo_int = _safe_int(codigo)
    desc_clean = str(descricao or "").strip()
    if codigo_int is None:
        return desc_clean or ""
    if not desc_clean:
        return str(codigo_int)
    return f"{codigo_int} - {desc_clean}"


def _query_eventos(*, alias: str, banco: str, codigo_empresa: int, somente_ativos: bool):
    qs = (
        Eventos.objects.using(alias)
        .filter(registro=banco, even_empr=codigo_empresa)
        .order_by("even_codi")
    )
    if somente_ativos:
        qs = qs.filter(Q(even_inativo=False) | Q(even_inativo__isnull=True))
    return qs


def obter_evento_label(*, banco: str, db_alias: str = None, codigo_empresa: int = 1, codigo_evento=None) -> str:
    alias = db_alias or "default"
    banco_limpo = _digits_only(banco)
    codigo_int = _safe_int(codigo_evento)
    if codigo_int is None:
        return ""
    try:
        evento = (
            _query_eventos(
                alias=alias,
                banco=banco_limpo,
                codigo_empresa=int(codigo_empresa or 1),
                somente_ativos=False,
            )
            .filter(even_codi=codigo_int)
            .values_list("even_codi", "even_desc")
            .first()
        )
    except Exception:
        evento = None
    if not evento:
        return str(codigo_int)
    return _format_evento_label(evento[0], evento[1])


def _append_choice_if_missing(choices, valor_atual, label_atual):
    valor_int = _safe_int(valor_atual)
    if valor_int is None:
        return choices
    if any(_safe_int(valor) == valor_int for valor, _ in choices if str(valor or "").strip()):
        return choices
    label = str(label_atual or "").strip() or str(valor_int)
    return [*choices, (valor_int, label)]


def listar_eventos_choices(*, banco: str, db_alias: str = None, codigo_empresa: int = 1, valor_atual=None):
    alias = db_alias or "default"
    banco_limpo = _digits_only(banco)
    empresa = int(codigo_empresa or 1)
    choices = [("", "Selecione")]
    try:
        eventos = _query_eventos(
            alias=alias,
            banco=banco_limpo,
            codigo_empresa=empresa,
            somente_ativos=True,
        ).values_list("even_codi", "even_desc")
        for codigo, descricao in eventos:
            codigo_int = _safe_int(codigo)
            if codigo_int is None:
                continue
            choices.append((codigo_int, _format_evento_label(codigo_int, descricao)))
    except Exception:
        pass
    return _append_choice_if_missing(
        choices,
        valor_atual,
        obter_evento_label(
            banco=banco_limpo,
            db_alias=alias,
            codigo_empresa=empresa,
            codigo_evento=valor_atual,
        ),
    )


def mapa_eventos(*, banco: str, db_alias: str = None, codigo_empresa: int = 1) -> dict:
    alias = db_alias or "default"
    banco_limpo = _digits_only(banco)
    empresa = int(codigo_empresa or 1)
    saida = {}
    try:
        eventos = _query_eventos(
            alias=alias,
            banco=banco_limpo,
            codigo_empresa=empresa,
            somente_ativos=False,
        ).values_list("even_codi", "even_desc")
        for codigo, descricao in eventos:
            codigo_int = _safe_int(codigo)
            if codigo_int is None:
                continue
            saida[codigo_int] = _format_evento_label(codigo_int, descricao)
    except Exception:
        return {}
    return saida


class EventosAgrupadosService:
    @staticmethod
    def obter(*, banco: str, even_empr: int, even_fili: int, db_alias: str = None):
        alias = db_alias or "default"
        banco_limpo = _digits_only(banco)
        columns = _get_table_columns(alias)
        selected_fields = [
            field for field in EventosAgrupados._meta.local_concrete_fields
            if field.column in columns
        ]
        if not selected_fields:
            return None

        sql = (
            "SELECT " + ", ".join(f'"{field.column}"' for field in selected_fields)
            + " FROM eventos_agrupados "
            + "WHERE registro = %s AND even_empr = %s AND even_fili = %s"
        )
        with connections[alias].cursor() as cur:
            cur.execute(sql, [banco_limpo, int(even_empr), int(even_fili)])
            row = cur.fetchone()
        if not row:
            return None

        row_map = {field.attname: value for field, value in zip(selected_fields, row)}
        data = {}
        for field in EventosAgrupados._meta.local_concrete_fields:
            data[field.attname] = row_map.get(field.attname, _model_default(field))
        obj = EventosAgrupados(**data)
        obj._state.adding = False
        obj._state.db = alias
        return obj

    @staticmethod
    def salvar_form(form, banco, db_alias, even_empr=None, even_fili=None, operacao=None):
        instance = form.save(commit=False)
        banco_limpo = _digits_only(banco)
        instance.registro = banco_limpo
        if even_empr is not None:
            instance.even_empr = even_empr
        if even_fili is not None:
            instance.even_fili = even_fili

        empr_i = int(getattr(instance, "even_empr") or 0)
        fili_i = int(getattr(instance, "even_fili") or 0)

        if operacao not in ("criar", "editar"):
            try:
                operacao = "editar" if getattr(form.instance, "pk", None) is not None else "criar"
            except Exception:
                operacao = "criar"

        qs_existente = EventosAgrupados.objects
        if db_alias:
            qs_existente = qs_existente.using(db_alias)
        duplicado = qs_existente.filter(
            registro=banco_limpo,
            even_empr=empr_i,
            even_fili=fili_i,
        ).exists()

        if operacao == "criar" and duplicado:
            raise ValidationError(
                "Ja existe uma configuracao de verbas agrupadas para a Empresa/Filial selecionada."
            )

        try:
            instance.save(using=db_alias, operacao=operacao)
        except TypeError:
            instance.save(using=db_alias)
        return instance

    @staticmethod
    def excluir(*, banco: str, even_empr: int, even_fili: int, db_alias: str = None):
        banco_limpo = _digits_only(banco)
        alias = db_alias or "default"
        sql = (
            "DELETE FROM eventos_agrupados "
            "WHERE registro = %s AND even_empr = %s AND even_fili = %s"
        )
        with connections[alias].cursor() as cur:
            cur.execute(sql, [str(banco_limpo), int(even_empr), int(even_fili)])

    @staticmethod
    def obter_nome_empresa(*, banco: str, db_alias: str = None, codigo_empresa=None) -> str:
        if not codigo_empresa:
            return ""
        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)
        empresa = (
            qs.filter(registro=_digits_only(banco), empr_empr=codigo_empresa)
            .order_by("empr_fili", "empr_nome")
            .first()
        )
        return getattr(empresa, "empr_nome", "") or ""

    @staticmethod
    def obter_nome_filial(*, banco: str, db_alias: str = None, codigo_empresa=None, codigo_filial=None) -> str:
        if not codigo_empresa or not codigo_filial:
            return ""
        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)
        filial = (
            qs.filter(
                registro=_digits_only(banco),
                empr_empr=codigo_empresa,
                empr_fili=codigo_filial,
            )
            .first()
        )
        return getattr(filial, "empr_fili_descr", "") or getattr(filial, "empr_nome", "") or ""

    @staticmethod
    def listar(*, banco: str, db_alias: str = None, codigo_empresa: int = 1, codigo_filial: int = 1) -> list:
        banco_limpo = _digits_only(banco)
        empr = int(codigo_empresa or 1)
        fili = int(codigo_filial or 1)
        alias = db_alias or "default"
        columns = _get_table_columns(alias)
        rows = []
        try:
            with connections[alias].cursor() as cur:
                sql = (
                    "SELECT "
                    + _sql_expr(columns, "even_empr", "NULL") + ", "
                    + _sql_expr(columns, "even_fili", "NULL") + ", "
                    + _sql_expr(columns, "even_ferias_proporcionais", "NULL") + ", "
                    + _sql_expr(columns, "even_ferias_vencidas", "NULL") + ", "
                    + _sql_expr(columns, "even_ferias_dobro", "NULL") + ", "
                    + _sql_expr(columns, "even_ferias_indenizadas", "NULL") + ", "
                    + _sql_expr(columns, "even_13_salario", "NULL") + ", "
                    + _sql_expr(columns, "even_13_salario_indenizado", "NULL") + ", "
                    + _sql_expr(columns, "even_aviso_previo_indenizado", "NULL")
                    + " FROM eventos_agrupados "
                    + "WHERE registro=%s AND even_empr=%s AND even_fili=%s"
                )
                cur.execute(sql, [banco_limpo, empr, fili])
                rows = cur.fetchall() or []
        except Exception:
            rows = []

        mapa = mapa_eventos(banco=banco_limpo, db_alias=alias, codigo_empresa=empr)
        saida = []
        for row in rows:
            item = {
                "even_empr": _safe_int(row[0]),
                "even_fili": _safe_int(row[1]),
                "even_ferias_proporcionais": _safe_int(row[2]),
                "even_ferias_vencidas": _safe_int(row[3]),
                "even_ferias_dobro": _safe_int(row[4]),
                "even_ferias_indenizadas": _safe_int(row[5]),
                "even_13_salario": _safe_int(row[6]),
                "even_13_salario_indenizado": _safe_int(row[7]),
                "even_aviso_previo_indenizado": _safe_int(row[8]),
            }
            for field in EVENTO_FIELDS:
                codigo = item.get(field)
                item[f"{field}_desc"] = mapa.get(codigo, "-") if codigo else "-"
            saida.append(item)
        return saida
