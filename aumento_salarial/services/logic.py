import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import connections
from django.db.models import IntegerField, Max
from django.db.models.functions import Coalesce

from aumento_salarial.models import AumentoSalarial
from cargos.services.logic import CargosService
from departamentosrh.services.logic import DepartamentosRhService
from empresas.models import Empresas
from funcionarios.models import ClassesFuncionario, Funcionarios
from setores.models import Setoresrh
from sindicatos.services.logic import SindicatoTrabalhadoresService


FORMA_CHOICES = (
    ("", "Selecione"),
    ("V", "Valor"),
    ("P", "Percentual"),
)

TIPO_FUNCIONARIO_RADIO_CHOICES = (
    ("T", "Todos"),
    ("M", "Mensalistas"),
    ("D", "Diaristas"),
    ("H", "Horistas"),
)

_TABLE_COLUMNS_CACHE = {}


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def _safe_int(value):
    try:
        if value is None:
            return None
        text = str(value).strip()
        if not text or not text.lstrip("-").isdigit():
            return None
        return int(text)
    except Exception:
        return None


def _safe_decimal(value):
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value).replace(".", "").replace(",", ".")) if "," in str(value) else Decimal(str(value))
    except Exception:
        try:
            return Decimal(str(value))
        except Exception:
            return None


def _model_default(field):
    internal_type = field.get_internal_type()
    if internal_type in ("BooleanField", "NullBooleanField"):
        return False
    if internal_type in ("CharField", "TextField"):
        return ""
    return None


def _get_table_columns(alias: str, table_name: str = "aumento_salarial") -> set:
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


def forma_label(value):
    current = str(value or "").strip().upper()
    for codigo, descricao in FORMA_CHOICES:
        if codigo == current:
            return descricao
    return current or "-"


def tipo_funcionario_label(value):
    current = str(value or "").strip().upper()
    for codigo, descricao in TIPO_FUNCIONARIO_RADIO_CHOICES:
        if codigo == current:
            return descricao
    return current or "-"


def proximo_codigo_aumento_salarial(*, banco: str, db_alias: str, empresa: int, filial: int) -> int:
    banco_limpo = _digits_only(banco)
    qs = AumentoSalarial.objects
    if db_alias:
        qs = qs.using(db_alias)
    max_codi = (
        qs.filter(registro=banco_limpo, aume_empr=int(empresa), aume_fili=int(filial))
        .aggregate(maximo=Coalesce(Max("aume_codi", output_field=IntegerField()), 0))
        .get("maximo")
        or 0
    )
    return int(max_codi) + 1


def listar_funcionarios_choices(*, banco: str, db_alias: str = None, codigo_empresa: int = 1, codigo_filial: int = 1, valor_atual=None):
    banco_limpo = _digits_only(banco)
    alias = db_alias or "default"
    choices = [("", "Selecione")]
    valor_int = _safe_int(valor_atual)
    try:
        rows = list(
            Funcionarios.objects.using(alias)
            .filter(
                registro=banco_limpo,
                func_empr=int(codigo_empresa),
                func_fili=int(codigo_filial),
            )
            .filter(func_data_saida__isnull=True)
            .order_by("func_nome", "func_codi")
            .values_list("func_codi", "func_nome")
        )
    except Exception:
        rows = []
        try:
            with connections[alias].cursor() as cur:
                cur.execute(
                    "SELECT func_codi, func_nome "
                    "FROM funcionarios "
                    "WHERE registro=%s AND func_empr=%s AND func_fili=%s "
                    "  AND func_data_saida IS NULL "
                    "ORDER BY func_nome, func_codi",
                    [banco_limpo, int(codigo_empresa), int(codigo_filial)],
                )
                rows = cur.fetchall() or []
        except Exception:
            rows = []
    if valor_int is not None:
        try:
            row_atual = (
                Funcionarios.objects.using(alias)
                .filter(
                    registro=banco_limpo,
                    func_empr=int(codigo_empresa),
                    func_fili=int(codigo_filial),
                    func_codi=valor_int,
                )
                .values_list("func_codi", "func_nome")
                .first()
            )
        except Exception:
            row_atual = None
        if not row_atual:
            try:
                with connections[alias].cursor() as cur:
                    cur.execute(
                        "SELECT func_codi, func_nome "
                        "FROM funcionarios "
                        "WHERE registro=%s AND func_empr=%s AND func_fili=%s AND func_codi=%s",
                        [banco_limpo, int(codigo_empresa), int(codigo_filial), valor_int],
                    )
                    row_atual = cur.fetchone()
            except Exception:
                row_atual = None
        if row_atual and not any(_safe_int(item[0]) == valor_int for item in rows):
            rows.append(row_atual)
    vistos = set()
    for codigo, nome in rows:
        codigo_int = _safe_int(codigo)
        if codigo_int is None or codigo_int in vistos:
            continue
        vistos.add(codigo_int)
        label = f"{codigo_int} - {str(nome or '').strip() or 'Funcionario'}"
        choices.append((codigo_int, label))
    if valor_int is not None and not any(_safe_int(valor) == valor_int for valor, _ in choices if str(valor).strip()):
        choices.append((valor_int, f"{valor_int} - Funcionario #{valor_int} (atual)"))
    return choices


def obter_funcionario_label(*, banco: str, db_alias: str = None, codigo_empresa: int = 1, codigo_filial: int = 1, codigo_funcionario=None) -> str:
    banco_limpo = _digits_only(banco)
    codigo_int = _safe_int(codigo_funcionario)
    if codigo_int is None:
        return ""
    alias = db_alias or "default"
    try:
        row = (
            Funcionarios.objects.using(alias)
            .filter(
                registro=banco_limpo,
                func_empr=int(codigo_empresa),
                func_fili=int(codigo_filial),
                func_codi=codigo_int,
            )
            .values_list("func_codi", "func_nome")
            .first()
        )
    except Exception:
        row = None
    if not row:
        return str(codigo_int)
    return f"{int(row[0])} - {str(row[1] or '').strip() or 'Funcionario'}"


def listar_classes_choices(*, db_alias: str = None, valor_atual=None):
    alias = db_alias or "default"
    choices = [("", "Selecione")]
    try:
        rows = list(
            ClassesFuncionario.objects.using(alias)
            .order_by("clas_codi")
            .values_list("clas_codi", "clas_desc")
        )
    except Exception:
        rows = []
    vistos = set()
    for codigo, descricao in rows:
        codigo_int = _safe_int(codigo)
        if codigo_int is None or codigo_int in vistos:
            continue
        vistos.add(codigo_int)
        label = f"{codigo_int} - {str(descricao or '').strip() or 'Classe'}"
        choices.append((codigo_int, label))
    valor_int = _safe_int(valor_atual)
    if valor_int is not None and not any(_safe_int(valor) == valor_int for valor, _ in choices if str(valor).strip()):
        choices.append((valor_int, f"{valor_int} - Classe #{valor_int} (atual)"))
    return choices


def listar_centro_custo_choices(*, banco: str, db_alias: str = None, codigo_empresa: int = 1, valor_atual=None):
    banco_limpo = _digits_only(banco)
    alias = db_alias or "default"
    choices = [("", "Selecione")]
    rows = []
    try:
        rows = list(
            Setoresrh.objects.using(alias)
            .filter(registro=banco_limpo, seto_empr=int(codigo_empresa), seto_cecu__isnull=False)
            .order_by("seto_cecu", "seto_desc")
            .values_list("seto_cecu", "seto_desc")
        )
    except Exception:
        rows = []
    vistos = set()
    for codigo, descricao in rows:
        codigo_int = _safe_int(codigo)
        if codigo_int is None or codigo_int in vistos:
            continue
        vistos.add(codigo_int)
        desc_clean = str(descricao or "").strip()
        label = f"{codigo_int} - {desc_clean}" if desc_clean else str(codigo_int)
        choices.append((codigo_int, label))
    valor_int = _safe_int(valor_atual)
    if valor_int is not None and not any(_safe_int(valor) == valor_int for valor, _ in choices if str(valor).strip()):
        choices.append((valor_int, str(valor_int)))
    return choices


class AumentoSalarialService:
    @staticmethod
    def obter(*, banco: str, aume_empr: int, aume_fili: int, aume_codi: int, db_alias: str = None):
        alias = db_alias or "default"
        banco_limpo = _digits_only(banco)
        columns = _get_table_columns(alias)
        selected_fields = [
            field for field in AumentoSalarial._meta.local_concrete_fields
            if field.column in columns
        ]
        if not selected_fields:
            return None

        sql = (
            "SELECT " + ", ".join(f'"{field.column}"' for field in selected_fields)
            + " FROM aumento_salarial "
            + "WHERE registro = %s AND aume_empr = %s AND aume_fili = %s AND aume_codi = %s"
        )
        with connections[alias].cursor() as cur:
            cur.execute(sql, [banco_limpo, int(aume_empr), int(aume_fili), int(aume_codi)])
            row = cur.fetchone()
        if not row:
            return None

        row_map = {field.attname: value for field, value in zip(selected_fields, row)}
        data = {}
        for field in AumentoSalarial._meta.local_concrete_fields:
            data[field.attname] = row_map.get(field.attname, _model_default(field))
        obj = AumentoSalarial(**data)
        obj._state.adding = False
        obj._state.db = alias
        return obj

    @staticmethod
    def salvar_form(form, banco, db_alias, aume_empr=None, aume_fili=None, operacao=None, **kwargs):
        instance = form.save(commit=False)
        banco_limpo = _digits_only(banco)
        instance.registro = banco_limpo
        if aume_empr is not None:
            instance.aume_empr = aume_empr
        if aume_fili is not None:
            instance.aume_fili = aume_fili

        usuario = kwargs.get("usuario") or kwargs.get("username") or ""
        try:
            usuario_str = str(getattr(usuario, "username", ""))[:30]
            if not usuario_str:
                usuario_str = str(usuario or "")[:30]
        except Exception:
            usuario_str = ""

        hoje = datetime.date.today()
        agora = datetime.datetime.now().time().replace(microsecond=0)

        empr_i = int(getattr(instance, "aume_empr") or 0)
        fili_i = int(getattr(instance, "aume_fili") or 0)
        codi_v = getattr(instance, "aume_codi", None)
        codi_i = int(codi_v) if str(codi_v or "").isdigit() else None

        if operacao not in ("criar", "editar"):
            try:
                operacao = "editar" if getattr(form.instance, "pk", None) is not None else "criar"
            except Exception:
                operacao = "criar"

        if operacao == "editar":
            obj_orig = getattr(form, "instance", None)
            if obj_orig is not None:
                orig_reg = getattr(obj_orig, "registro", None)
                orig_empr = getattr(obj_orig, "aume_empr", None)
                orig_fili = getattr(obj_orig, "aume_fili", None)
                orig_codi = getattr(obj_orig, "aume_codi", None)
                if orig_reg and not instance.registro:
                    instance.registro = orig_reg
                if str(orig_empr or "").isdigit() and not empr_i:
                    instance.aume_empr = int(orig_empr)
                    empr_i = int(instance.aume_empr)
                if str(orig_fili or "").isdigit() and not fili_i:
                    instance.aume_fili = int(orig_fili)
                    fili_i = int(instance.aume_fili)
                if str(orig_codi or "").isdigit() and codi_i is None:
                    instance.aume_codi = int(orig_codi)
                    codi_i = int(instance.aume_codi)

        if operacao == "criar":
            if codi_i is None or codi_i <= 0:
                instance.aume_codi = proximo_codigo_aumento_salarial(
                    banco=banco_limpo,
                    db_alias=db_alias,
                    empresa=empr_i,
                    filial=fili_i,
                )
                codi_i = int(instance.aume_codi)
            qs_existente = AumentoSalarial.objects
            if db_alias:
                qs_existente = qs_existente.using(db_alias)
            duplicado = qs_existente.filter(
                registro=banco_limpo,
                aume_empr=empr_i,
                aume_fili=fili_i,
                aume_codi=codi_i,
            ).exists()
            if duplicado:
                raise ValidationError(
                    f"Ja existe um aumento salarial cadastrado com o Codigo {codi_i} para a Empresa/Filial selecionada."
                )
            instance.aume_usuario_inc = usuario_str or None
            instance.aume_data_inc = hoje
            if not getattr(instance, "aume_data_alteracao", None):
                instance.aume_data_alteracao = hoje
        else:
            instance.aume_usuario_alt = usuario_str or None
            instance.aume_data_alt = hoje

        instance.log_data = hoje
        instance.log_hora = agora

        try:
            instance.save(using=db_alias, operacao=operacao)
        except TypeError:
            instance.save(using=db_alias)
        return instance

    @staticmethod
    def excluir(*, banco: str, aume_empr: int, aume_fili: int, aume_codi: int, db_alias: str = None):
        banco_limpo = _digits_only(banco)
        alias = db_alias or "default"
        sql = (
            "DELETE FROM aumento_salarial "
            "WHERE registro = %s AND aume_empr = %s AND aume_fili = %s AND aume_codi = %s"
        )
        with connections[alias].cursor() as cur:
            cur.execute(sql, [str(banco_limpo), int(aume_empr), int(aume_fili), int(aume_codi)])

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
                    + _sql_expr(columns, "aume_codi", "NULL") + ", "
                    + _sql_expr(columns, "aume_desc", "''") + ", "
                    + _sql_expr(columns, "aume_func", "NULL") + ", "
                    + _sql_expr(columns, "aume_tipo_funcionario", "''") + ", "
                    + _sql_expr(columns, "aume_data_alteracao", "NULL") + ", "
                    + _sql_expr(columns, "aume_data_efeito", "NULL") + ", "
                    + _sql_expr(columns, "aume_forma", "''") + ", "
                    + _sql_expr(columns, "aume_valor", "NULL")
                    + " FROM aumento_salarial "
                    + "WHERE registro=%s AND aume_empr=%s AND aume_fili=%s "
                    + "ORDER BY aume_codi"
                )
                cur.execute(sql, [banco_limpo, empr, fili])
                rows = cur.fetchall() or []
        except Exception:
            rows = []

        funcionarios_map = {
            _safe_int(valor): label
            for valor, label in listar_funcionarios_choices(
                banco=banco_limpo,
                db_alias=alias,
                codigo_empresa=empr,
                codigo_filial=fili,
            )
            if str(valor).strip()
        }
        saida = []
        vistos = set()
        for codi, desc, func, tipo_funcionario, data_alt, data_efeito, forma, valor in rows:
            codi_int = _safe_int(codi)
            if codi_int is None or codi_int in vistos:
                continue
            vistos.add(codi_int)
            func_int = _safe_int(func)
            tipo_func_clean = str(tipo_funcionario or "").strip().upper()
            funcionario_nome = funcionarios_map.get(func_int, "") if func_int is not None else ""
            if not funcionario_nome:
                funcionario_nome = tipo_funcionario_label(tipo_func_clean)
            saida.append({
                "aume_codi": codi_int,
                "aume_desc": str(desc or "").strip(),
                "aume_func": func_int,
                "aume_tipo_funcionario": tipo_func_clean,
                "aume_tipo_funcionario_desc": tipo_funcionario_label(tipo_func_clean),
                "funcionario_nome": funcionario_nome,
                "aume_data_alteracao": data_alt,
                "aume_data_efeito": data_efeito,
                "aume_forma": str(forma or "").strip(),
                "aume_forma_desc": forma_label(forma),
                "aume_valor": valor,
            })
        return saida

    @staticmethod
    def choices_classes(*, db_alias: str = None, valor_atual=None) -> list:
        return listar_classes_choices(db_alias=db_alias, valor_atual=valor_atual)

    @staticmethod
    def choices_cargos(*, banco: str, db_alias: str = None, codigo_empresa: int = 1, codigo_filial: int = 1, valor_atual=None) -> list:
        return CargosService.choices_cargos(
            banco=banco,
            db_alias=db_alias,
            codigo_empresa=codigo_empresa,
            codigo_filial=codigo_filial,
            incluir_selecione=True,
            valor_atual=valor_atual,
            incluir_inativos=True,
        )

    @staticmethod
    def choices_departamentos(*, banco: str, db_alias: str = None, codigo_empresa: int = 1, codigo_filial: int = 1, valor_atual=None) -> list:
        return DepartamentosRhService.choices_departamentos(
            banco=banco,
            db_alias=db_alias,
            codigo_empresa=codigo_empresa,
            codigo_filial=codigo_filial,
            incluir_selecione=True,
            valor_atual=valor_atual,
            incluir_inativos=True,
        )

    @staticmethod
    def choices_sindicatos(*, banco: str, db_alias: str = None, codigo_empresa: int = 1, codigo_filial: int = 1, valor_atual=None) -> list:
        return SindicatoTrabalhadoresService.choices_sindicatos(
            banco=banco,
            db_alias=db_alias,
            codigo_empresa=codigo_empresa,
            codigo_filial=codigo_filial,
            incluir_selecione=True,
            valor_atual=valor_atual,
        )

    @staticmethod
    def choices_centro_custo(*, banco: str, db_alias: str = None, codigo_empresa: int = 1, valor_atual=None) -> list:
        return listar_centro_custo_choices(
            banco=banco,
            db_alias=db_alias,
            codigo_empresa=codigo_empresa,
            valor_atual=valor_atual,
        )
