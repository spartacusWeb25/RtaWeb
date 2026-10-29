from django.db import connections
from django.db.models import Max, IntegerField
from django.db.models.functions import Coalesce
from django.core.exceptions import ValidationError
from types import SimpleNamespace

from empresas.models import Empresas
from prepara_rescisoes.models import PreparaRescisoes
from prepara_rescisoes.web.forms import (
    CHOICES_CAGED_MOTIVOS,
    CHOICES_FGTS_MOTIVOS,
    _MAP_AVISO_PREVIO_DESC,
    _MAP_INICIATIVA_DESC,
)


_TABLE_COLUMNS_CACHE = {}
_MAP_FGTS_DESC = {str(cod): desc for cod, desc in CHOICES_FGTS_MOTIVOS if str(cod or "").strip()}
_MAP_CAGED_DESC = {str(cod): desc for cod, desc in CHOICES_CAGED_MOTIVOS if str(cod or "").strip()}


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def _get_table_columns(alias: str, table_name: str = "prepara_rescisoes") -> set:
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
    if internal_type in ("BooleanField", "NullBooleanField"):
        return False
    if internal_type in ("CharField", "TextField"):
        return ""
    return None


def proximo_codigo_prepara_rescisao(*, banco: str, db_alias: str, empresa: int, filial: int) -> int:
    banco_limpo = _digits_only(banco)
    qs = PreparaRescisoes.objects
    if db_alias:
        qs = qs.using(db_alias)
    max_codi = (
        qs.filter(registro=banco_limpo, prep_empr=int(empresa), prep_fili=int(filial))
        .aggregate(maximo=Coalesce(Max("prep_codi", output_field=IntegerField()), 0))
        .get("maximo") or 0
    )
    return int(max_codi) + 1


class PreparaRescisoesService:

    @staticmethod
    def obter(*, banco: str, prep_empr: int, prep_fili: int, prep_codi: int, db_alias: str = None):
        alias = db_alias or "default"
        banco_limpo = _digits_only(banco)
        columns = _get_table_columns(alias)
        selected_fields = [
            field for field in PreparaRescisoes._meta.local_concrete_fields
            if field.column in columns
        ]
        if not selected_fields:
            return None

        sql = (
            "SELECT " + ", ".join(f'"{field.column}"' for field in selected_fields)
            + " FROM prepara_rescisoes "
            + "WHERE registro = %s AND prep_empr = %s AND prep_fili = %s AND prep_codi = %s"
        )
        with connections[alias].cursor() as cur:
            cur.execute(sql, [banco_limpo, int(prep_empr), int(prep_fili), int(prep_codi)])
            row = cur.fetchone()
        if not row:
            return None

        row_map = {
            field.attname: value
            for field, value in zip(selected_fields, row)
        }
        data = {}
        for field in PreparaRescisoes._meta.local_concrete_fields:
            data[field.attname] = row_map.get(field.attname, _model_default(field))
        obj = PreparaRescisoes(**data)
        obj._state.adding = False
        obj._state.db = alias
        return obj

    @staticmethod
    def salvar_form(form, banco, db_alias, prep_empr=None, prep_fili=None, operacao=None, **kwargs):
        instance = form.save(commit=False)
        banco_limpo = _digits_only(banco)
        instance.registro = banco_limpo
        if prep_empr is not None:
            instance.prep_empr = prep_empr
        if prep_fili is not None:
            instance.prep_fili = prep_fili

        import datetime
        usuario = kwargs.get("usuario") or kwargs.get("username") or ""
        try:
            usuario_str = str(getattr(usuario, "username", ""))[:30]
            if not usuario_str:
                usuario_str = str(usuario or "")[:30]
        except Exception:
            usuario_str = ""

        today = datetime.date.today()

        empr_i = int(getattr(instance, "prep_empr") or 0)
        fili_i = int(getattr(instance, "prep_fili") or 0)
        codi_v = getattr(instance, "prep_codi", None)
        codi_i = int(codi_v) if str(codi_v or "").isdigit() else None

        if operacao not in ("criar", "editar"):
            try:
                modo_instancia = getattr(form.instance, "pk", None)
                operacao = "editar" if modo_instancia is not None else "criar"
            except Exception:
                operacao = "criar"

        if operacao == "editar":
            obj_orig = getattr(form, "instance", None)
            if obj_orig is not None:
                orig_reg = getattr(obj_orig, "registro", None)
                orig_empr = getattr(obj_orig, "prep_empr", None)
                orig_fili = getattr(obj_orig, "prep_fili", None)
                orig_codi = getattr(obj_orig, "prep_codi", None)
                if orig_reg and not instance.registro:
                    instance.registro = orig_reg
                e_tmp = int(orig_empr) if str(orig_empr or "").isdigit() else None
                if e_tmp and (not empr_i or empr_i == 0):
                    instance.prep_empr = e_tmp
                    empr_i = int(instance.prep_empr)
                f_tmp = int(orig_fili) if str(orig_fili or "").isdigit() else None
                if f_tmp and (not fili_i or fili_i == 0):
                    instance.prep_fili = f_tmp
                    fili_i = int(instance.prep_fili)
                c_tmp = int(orig_codi) if str(orig_codi or "").isdigit() else None
                if c_tmp and (not codi_i or codi_i is None):
                    instance.prep_codi = c_tmp
                    codi_i = int(instance.prep_codi)

        if operacao == "criar":
            if codi_i is None or codi_i <= 0:
                instance.prep_codi = proximo_codigo_prepara_rescisao(
                    banco=banco_limpo,
                    db_alias=db_alias,
                    empresa=empr_i,
                    filial=fili_i,
                )
                codi_i = int(instance.prep_codi)
            qs_existente = PreparaRescisoes.objects
            if db_alias:
                qs_existente = qs_existente.using(db_alias)
            duplicado = qs_existente.filter(
                registro=banco_limpo,
                prep_empr=empr_i,
                prep_fili=fili_i,
                prep_codi=codi_i,
            ).exists()
            if duplicado:
                raise ValidationError(
                    f"Já existe uma Preparação de Rescisão cadastrada com o Código {codi_i} "
                    "para a Empresa/Filial selecionada."
                )
            instance.prep_usuario_inc = usuario_str or None
            instance.prep_data_inc = today
        else:
            instance.prep_usuario_alt = usuario_str or None
            instance.prep_data_alt = today

        try:
            instance.save(using=db_alias, operacao=operacao)
        except TypeError:
            instance.save(using=db_alias)
        return instance

    @staticmethod
    def excluir(*, banco: str, prep_empr: int, prep_fili: int, prep_codi: int, db_alias: str = None):
        from django.db import connections

        banco_limpo = _digits_only(banco)
        alias = db_alias or "default"
        sql = (
            "DELETE FROM prepara_rescisoes "
            "WHERE registro = %s AND prep_empr = %s AND prep_fili = %s AND prep_codi = %s"
        )
        params = [
            str(banco_limpo),
            int(prep_empr),
            int(prep_fili),
            int(prep_codi),
        ]
        with connections[alias].cursor() as cur:
            cur.execute(sql, params)

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
        return (getattr(filial, "empr_fili_descr", "")
                or getattr(filial, "empr_nome", "")
                or "")

    @staticmethod
    def obter_empresa_padrao(*, banco: str, db_alias: str = None):
        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)
        return (
            qs.filter(registro=_digits_only(banco))
            .order_by("empr_empr", "empr_fili", "empr_nome")
            .first()
        )

    @staticmethod
    def listar(*, banco: str, db_alias: str = None,
               codigo_empresa: int = 1, codigo_filial: int = 1,
               incluir_inativos: bool = True) -> list:
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
                    + _sql_expr(columns, "prep_codi", "NULL") + ", "
                    + _sql_expr(columns, "prep_desc", "''") + ", "
                    + _sql_expr(columns, "prep_descricao", "''") + ", "
                    + _sql_expr(columns, "prep_iniciativa_codi", "NULL") + ", "
                    + _sql_expr(columns, "prep_aviso_previo_codi", "NULL") + ", "
                    + _sql_expr(columns, "prep_fgts_codi", "''") + ", "
                    + _sql_expr(columns, "prep_caged_codi", "''") + ", "
                    + _sql_expr(columns, "prep_inden_ferias_13", "FALSE") + ", "
                    + _sql_expr(columns, "prep_inativo", "FALSE") + ", "
                    + _sql_expr(columns, "prep_motivo_esocial_codi", "''") + ", "
                    + _sql_expr(columns, "prep_motivo_esocial_desc", "''")
                    + " FROM prepara_rescisoes "
                    + "WHERE registro=%s AND prep_empr=%s AND prep_fili=%s"
                )
                if not incluir_inativos and "prep_inativo" in columns:
                    sql += " AND COALESCE(prep_inativo, FALSE) = FALSE"
                sql += " ORDER BY prep_codi"
                cur.execute(sql, [banco_limpo, empr, fili])
                rows = cur.fetchall() or []
        except Exception:
            rows = []
        saida = []
        vistos = set()
        for cod, desc_tit, desc_comp, iniciativa_codi, aviso_codi, fgts_codi, caged_codi, inden_13, inativo, ms_cod, ms_desc in rows:
            cod_clean = str(int(cod or 0))
            if not cod_clean or cod_clean in vistos:
                continue
            vistos.add(cod_clean)
            desc_tit_clean = str(desc_tit or "").strip()
            desc_comp_clean = str(desc_comp or "").strip()
            iniciativa_desc = _MAP_INICIATIVA_DESC.get(str(int(iniciativa_codi)), "") if iniciativa_codi not in (None, "") else ""
            aviso_desc = _MAP_AVISO_PREVIO_DESC.get(str(int(aviso_codi)), "") if aviso_codi not in (None, "") else ""
            fgts_desc = _MAP_FGTS_DESC.get(str(fgts_codi or "").strip(), "")
            caged_desc = _MAP_CAGED_DESC.get(str(caged_codi or "").strip(), "")
            label = desc_comp_clean or desc_tit_clean or f"Preparação de Rescisão #{cod_clean}"
            saida.append({
                "prep_codi": int(cod_clean),
                "prep_desc": desc_tit_clean,
                "prep_descricao": desc_comp_clean,
                "prep_iniciativa_desc": iniciativa_desc,
                "prep_aviso_previo_desc": aviso_desc,
                "prep_fgts_desc": fgts_desc,
                "prep_caged_desc": caged_desc,
                "prep_inden_ferias_13": bool(inden_13),
                "prep_motivo_esocial_codi": str(ms_cod or "").strip(),
                "prep_motivo_esocial_desc": str(ms_desc or "").strip(),
                "label": label,
                "prep_inativo": bool(inativo),
            })
        return saida

    @staticmethod
    def choices(*, banco: str, db_alias: str = None,
                codigo_empresa: int = 1, codigo_filial: int = 1,
                incluir_selecione: bool = True, valor_atual=None,
                incluir_inativos: bool = True) -> list:
        lista = PreparaRescisoesService.listar(
            banco=banco, db_alias=db_alias,
            codigo_empresa=codigo_empresa, codigo_filial=codigo_filial,
            incluir_inativos=incluir_inativos,
        )
        choices = []
        if incluir_selecione:
            choices.append((None, "Selecione"))
        for item in lista:
            codi_int = int(item["prep_codi"])
            rotulo = f"{item['prep_codi']} - {item['label']}"
            if item.get("prep_inativo"):
                rotulo = f"{rotulo} (Inativo)"
            choices.append((codi_int, rotulo))
        if valor_atual is not None:
            try:
                val_int = int(valor_atual)
                existe = any(int(ch) == val_int for ch, _ in choices if ch is not None)
                if not existe and val_int > 0:
                    choices.append((val_int, f"{val_int} - Preparação #{val_int} (atual)"))
            except Exception:
                pass
        return choices
