from django.core.exceptions import ValidationError
from django.db import connection

from empresas.models import Empresas


def _digits_only(valor) -> str:
    if valor is None:
        return ""
    return "".join(ch for ch in str(valor) if ch.isdigit())


def _safe_int(valor, default=0):
    try:
        if valor is None or valor == "":
            return default
        return int(str(valor).strip())
    except (TypeError, ValueError):
        try:
            digits = _digits_only(valor)
            if not digits:
                return default
            return int(digits)
        except Exception:
            return default


class HorariosService:

    @staticmethod
    def proximo_codigo_quadro(*, banco: str, db_alias: str = None,
                               empr_codigo: int = 1, fili_codigo: int = 1) -> int:
        banco_limpo = _digits_only(banco)
        empr = _safe_int(empr_codigo)
        fili = _safe_int(fili_codigo)
        sql = (
            "SELECT COALESCE(MAX(hora_codi), 0) FROM public.horarios "
            "WHERE registro=%s AND hora_empr=%s AND hora_fili=%s"
        )
        with connection.cursor() as cursor:
            cursor.execute(sql, [banco_limpo, empr, fili])
            row = cursor.fetchone()
        atual = int(row[0] or 0) if row else 0
        return atual + 1

    @staticmethod
    def obter_nome_empresa(*, banco: str, db_alias: str = None,
                           codigo_empresa=None) -> str:
        if not codigo_empresa:
            return ""
        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)
        empresa = (
            qs.filter(registro=_digits_only(banco), empr_empr=int(codigo_empresa))
            .order_by("empr_fili", "empr_nome")
            .first()
        )
        return getattr(empresa, "empr_nome", "") or ""

    @staticmethod
    def obter_nome_filial(*, banco: str, db_alias: str = None,
                          codigo_empresa=None, codigo_filial=None) -> str:
        if not codigo_empresa or not codigo_filial:
            return ""
        qs = Empresas.objects
        if db_alias:
            qs = qs.using(db_alias)
        filial = (
            qs.filter(
                registro=_digits_only(banco),
                empr_empr=int(codigo_empresa),
                empr_fili=int(codigo_filial),
            )
            .first()
        )
        return getattr(filial, "empr_fili_descr", "") or getattr(filial, "empr_nome", "") or ""

    @staticmethod
    def obter_quadro_raw(*, banco: str, hora_codi, db_alias: str = None,
                         empr_codigo: int = 1, fili_codigo: int = 1) -> dict:
        banco_limpo = _digits_only(banco)
        empr = _safe_int(empr_codigo)
        fili = _safe_int(fili_codigo)
        codi = _safe_int(hora_codi)
        if codi <= 0 or not banco_limpo:
            return {}
        dias = ["dom", "seg", "ter", "qua", "qui", "sex", "sab"]
        campos_hora = [
            "esoc",
            "inic_1", "fina_1",
            "lanc_inic_1", "lanc_fina_1",
            "inic_2", "fina_2",
            "lanc_inic_2", "lanc_fina_2",
            "intervalo", "jornada",
        ]
        colunas = [
            "registro", "hora_empr", "hora_fili", "hora_codi",
            "hora_nome", "hora_flexivel", "hora_total_semana",
            "hora_folga_alt", "hora_desc_esocial",
        ]
        for d in dias:
            colunas.append(f"hora_folga_{d}")
            for c in campos_hora:
                colunas.append(f"hora_{d}_{c}")
        colunas_sql = ", ".join(colunas)
        sql = (
            f"SELECT {colunas_sql} FROM public.horarios "
            "WHERE registro=%s AND hora_empr=%s AND hora_fili=%s AND hora_codi=%s "
            "LIMIT 1"
        )
        params = [banco_limpo, empr, fili, codi]
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            row = cursor.fetchone()
            if row is None:
                return {}
            values = list(row)
        resultado = {}
        for idx, col in enumerate(colunas):
            if idx >= len(values):
                resultado[col] = None
                continue
            v = values[idx]
            if isinstance(v, memoryview):
                try:
                    v = bytes(v).decode("utf-8")
                except Exception:
                    v = None
            resultado[col] = v
        return resultado

    @staticmethod
    def salvar_form(*, form, operacao: str, banco: str,
                    db_alias: str = None, empr_codigo: int = 1,
                    fili_codigo: int = 1):
        banco_limpo = _digits_only(banco)
        empr = _safe_int(empr_codigo)
        fili = _safe_int(fili_codigo)

        if not form.is_valid():
            raise ValidationError(
                "Verifique os campos em destaque antes de salvar."
            )

        cleaned = getattr(form, "cleaned_data", None) or {}

        codi_proposto = _safe_int(cleaned.get("hora_codi", 0) or 0)
        if codi_proposto <= 0:
            orig = getattr(form, "instance", None)
            if orig is not None:
                codi_proposto = _safe_int(getattr(orig, "hora_codi", 0) or 0)
        if codi_proposto <= 0:
            codi_proposto = HorariosService.proximo_codigo_quadro(
                banco=banco,
                db_alias=db_alias,
                empr_codigo=empr,
                fili_codigo=fili,
            )
        if operacao == "editar":
            orig = getattr(form, "instance", None)
            if orig is not None:
                orig_codi = _safe_int(getattr(orig, "hora_codi", 0) or 0)
                if orig_codi > 0:
                    codi_proposto = orig_codi
                orig_empr = _safe_int(getattr(orig, "hora_empr", 0) or 0)
                if orig_empr > 0:
                    empr = orig_empr
                orig_fili = _safe_int(getattr(orig, "hora_fili", 0) or 0)
                if orig_fili > 0:
                    fili = orig_fili
                orig_reg = _digits_only(getattr(orig, "registro", None))
                if orig_reg:
                    banco_limpo = orig_reg

        dias = ["dom", "seg", "ter", "qua", "qui", "sex", "sab"]
        campos_hora_dia = [
            "esoc",
            "inic_1", "fina_1",
            "lanc_inic_1", "lanc_fina_1",
            "inic_2", "fina_2",
            "lanc_inic_2", "lanc_fina_2",
            "intervalo", "jornada",
        ]

        colunas_fix = [
            "registro", "hora_empr", "hora_fili", "hora_codi",
            "hora_nome", "hora_flexivel", "hora_total_semana",
            "hora_folga_alt",
            "hora_folga_dom", "hora_folga_seg", "hora_folga_ter",
            "hora_folga_qua", "hora_folga_qui", "hora_folga_sex", "hora_folga_sab",
            "hora_desc_esocial",
        ]
        colunas_dia = []
        for d in dias:
            for c in campos_hora_dia:
                colunas_dia.append(f"hora_{d}_{c}")
        colunas = colunas_fix + colunas_dia

        valores = {}
        valores["registro"] = banco_limpo
        valores["hora_empr"] = empr
        valores["hora_fili"] = fili
        valores["hora_codi"] = codi_proposto

        for col in ["hora_nome", "hora_total_semana", "hora_desc_esocial"]:
            v = cleaned.get(col, None)
            valores[col] = str(v).strip() if v not in (None, "") else None

        for col in ["hora_flexivel", "hora_folga_alt"]:
            v = cleaned.get(col, None)
            valores[col] = bool(v) if v is not None else False

        for col in ["hora_folga_dom", "hora_folga_seg", "hora_folga_ter",
                    "hora_folga_qua", "hora_folga_qui", "hora_folga_sex", "hora_folga_sab"]:
            v = cleaned.get(col, None)
            valores[col] = bool(v) if v is not None else False

        for d in dias:
            for c in campos_hora_dia:
                key = f"hora_{d}_{c}"
                v = cleaned.get(key, None)
                if c == "esoc":
                    if v in (None, ""):
                        valores[key] = None
                    else:
                        try:
                            valores[key] = int(v)
                        except Exception:
                            valores[key] = None
                else:
                    if v in (None, ""):
                        valores[key] = None
                    else:
                        sv = str(v).strip()
                        valores[key] = sv if sv else None

        existe_sql = (
            "SELECT 1 FROM public.horarios "
            "WHERE registro=%s AND hora_empr=%s AND hora_fili=%s AND hora_codi=%s "
            "LIMIT 1"
        )
        existe_params = [banco_limpo, empr, fili, codi_proposto]
        with connection.cursor() as cursor:
            cursor.execute(existe_sql, existe_params)
            existe = cursor.fetchone() is not None
        if operacao == "criar" and existe:
            raise ValidationError(
                f"Já existe Quadro de Horários com Código {codi_proposto} "
                "na Empresa/Filial selecionada."
            )
        if operacao == "editar" and not existe:
            operacao = "criar"

        if operacao == "criar":
            todas_cols = list(colunas) + ["_log_data", "_log_time"]
            placeholders_values = []
            params_sql = []
            for col in todas_cols:
                if col == "_log_data":
                    placeholders_values.append("CURRENT_DATE")
                elif col == "_log_time":
                    placeholders_values.append("CURRENT_TIME")
                else:
                    placeholders_values.append("%s")
                    params_sql.append(valores[col])
            sql = (
                f"INSERT INTO public.horarios ({', '.join(todas_cols)}) "
                f"VALUES ({', '.join(placeholders_values)})"
            )
            with connection.cursor() as cursor:
                cursor.execute(sql, params_sql)
        else:
            sets_cols = []
            params_sql = []
            for col in colunas_fix:
                if col in ("registro", "hora_empr", "hora_fili", "hora_codi"):
                    continue
                sets_cols.append(f"{col}=%s")
                params_sql.append(valores[col])
            for col in colunas_dia:
                sets_cols.append(f"{col}=%s")
                params_sql.append(valores[col])
            sets_cols.append("_log_data=CURRENT_DATE")
            sets_cols.append("_log_time=CURRENT_TIME")
            sql = (
                f"UPDATE public.horarios SET {', '.join(sets_cols)} "
                "WHERE registro=%s AND hora_empr=%s AND hora_fili=%s AND hora_codi=%s"
            )
            params_sql.extend([banco_limpo, empr, fili, codi_proposto])
            with connection.cursor() as cursor:
                cursor.execute(sql, params_sql)

        class HorarioSimplificado:
            def __init__(self_inner, **kwargs):
                for k, v in kwargs.items():
                    setattr(self_inner, k, v)
                for d in dias:
                    setattr(self_inner, f"hora_folga_{d}",
                            valores.get(f"hora_folga_{d}", False))
                    for c in campos_hora_dia:
                        setattr(self_inner, f"hora_{d}_{c}",
                                valores.get(f"hora_{d}_{c}", None))

            def delete(self_inner, *args, **kwargs):
                sql_del = (
                    "DELETE FROM public.horarios "
                    "WHERE registro=%s AND hora_empr=%s AND hora_fili=%s AND hora_codi=%s"
                )
                with connection.cursor() as cursor:
                    cursor.execute(sql_del, [
                        self_inner.registro,
                        int(self_inner.hora_empr),
                        int(self_inner.hora_fili),
                        int(self_inner.hora_codi),
                    ])

            @property
            def pk(self_inner):
                return (self_inner.registro, self_inner.hora_empr,
                        self_inner.hora_fili, self_inner.hora_codi)

        return HorarioSimplificado(
            registro=banco_limpo,
            hora_empr=empr,
            hora_fili=fili,
            hora_codi=codi_proposto,
            hora_nome=valores.get("hora_nome", None),
            hora_total_semana=valores.get("hora_total_semana", None),
            hora_flexivel=bool(valores.get("hora_flexivel", False)),
            hora_folga_alt=bool(valores.get("hora_folga_alt", False)),
            hora_desc_esocial=valores.get("hora_desc_esocial", None),
        )
