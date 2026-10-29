from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import connections
from django.db.models import Q

from empresas.models import Empresas
from eventos.models import Eventos


TIPO_CALCULO_CHOICES = (
    ("01", "Folha normal"),
    ("02", "13º salário"),
    ("03", "Férias"),
    ("04", "Rescisão"),
)

TIPO_CALCULO_LABELS = dict(TIPO_CALCULO_CHOICES)
TIPO_CALCULO_DEFAULT = "01"


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


def _normalizar_tipo_calculo(value):
    tipo = str(value or "").strip()
    if tipo in TIPO_CALCULO_LABELS:
        return tipo
    return TIPO_CALCULO_DEFAULT


def _formatar_evento(codigo, descricao):
    codigo_int = _safe_int(codigo)
    descricao_limpa = str(descricao or "").strip()
    if codigo_int is None:
        return descricao_limpa or ""
    if not descricao_limpa:
        return str(codigo_int)
    return f"{codigo_int} - {descricao_limpa}"


def _query_eventos(*, alias: str, banco: str, codigo_empresa: int, somente_ativos: bool):
    qs = (
        Eventos.objects.using(alias)
        .filter(registro=banco, even_empr=codigo_empresa)
        .order_by("even_codi")
    )
    if somente_ativos:
        qs = qs.filter(Q(even_inativo=False) | Q(even_inativo__isnull=True))
    return qs


class EventosAutomaticosService:
    @staticmethod
    def listar_eventos_choices(*, banco: str, db_alias: str = None, codigo_empresa: int = 1):
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
                choices.append((codigo_int, _formatar_evento(codigo_int, descricao)))
        except Exception:
            pass
        return choices

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
    def obter_nome_filial(
        *, banco: str, db_alias: str = None, codigo_empresa=None, codigo_filial=None
    ) -> str:
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
    def listar_por_tipo(
        *, banco: str, db_alias: str = None, codigo_empresa: int = 1, codigo_filial: int = 1
    ):
        alias = db_alias or "default"
        banco_limpo = _digits_only(banco)
        empresa = int(codigo_empresa or 1)
        filial = int(codigo_filial or 1)

        saida = {tipo: [] for tipo, _ in TIPO_CALCULO_CHOICES}
        sql = (
            "SELECT ea.even_tipo_calculo, ea.even_codi, ev.even_desc "
            "FROM eventos_automaticos ea "
            "LEFT JOIN eventos ev "
            "  ON ev.registro = ea.registro "
            " AND ev.even_empr = ea.even_empr "
            " AND ev.even_codi = ea.even_codi "
            "WHERE ea.registro = %s "
            "  AND ea.even_empr = %s "
            "  AND ea.even_fili = %s "
            "ORDER BY ea.even_tipo_calculo, ea.even_codi"
        )

        try:
            with connections[alias].cursor() as cur:
                cur.execute(sql, [banco_limpo, empresa, filial])
                for tipo, codigo, descricao in cur.fetchall() or []:
                    tipo_normalizado = _normalizar_tipo_calculo(tipo)
                    codigo_int = _safe_int(codigo)
                    if codigo_int is None:
                        continue
                    saida[tipo_normalizado].append(
                        {
                            "even_tipo_calculo": tipo_normalizado,
                            "even_tipo_calculo_desc": TIPO_CALCULO_LABELS.get(tipo_normalizado, ""),
                            "even_codi": codigo_int,
                            "even_desc": str(descricao or "").strip() or str(codigo_int),
                            "evento_label": _formatar_evento(codigo_int, descricao),
                        }
                    )
        except Exception:
            return saida
        return saida

    @staticmethod
    def adicionar_evento(
        *,
        banco: str,
        db_alias: str = None,
        codigo_empresa: int = 1,
        codigo_filial: int = 1,
        even_tipo_calculo: str,
        even_codi,
    ):
        alias = db_alias or "default"
        banco_limpo = _digits_only(banco)
        empresa = int(codigo_empresa or 1)
        filial = int(codigo_filial or 1)
        tipo = _normalizar_tipo_calculo(even_tipo_calculo)
        codigo_evento = _safe_int(even_codi)

        if codigo_evento is None:
            raise ValidationError("Selecione um evento para adicionar.")

        evento_existe = (
            _query_eventos(
                alias=alias,
                banco=banco_limpo,
                codigo_empresa=empresa,
                somente_ativos=True,
            )
            .filter(even_codi=codigo_evento)
            .exists()
        )
        if not evento_existe:
            raise ValidationError("O evento selecionado não está ativo para a empresa informada.")

        sql_existe = (
            "SELECT 1 "
            "FROM eventos_automaticos "
            "WHERE registro = %s "
            "  AND even_empr = %s "
            "  AND even_fili = %s "
            "  AND even_tipo_calculo = %s "
            "  AND even_codi = %s "
            "LIMIT 1"
        )
        with connections[alias].cursor() as cur:
            cur.execute(sql_existe, [banco_limpo, empresa, filial, tipo, codigo_evento])
            if cur.fetchone():
                raise ValidationError("Este evento já está cadastrado nesta aba.")

            agora = datetime.now()
            cur.execute(
                "INSERT INTO eventos_automaticos "
                "(registro, even_empr, even_fili, even_tipo_calculo, even_codi, _log_data, _log_time) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                [
                    banco_limpo,
                    empresa,
                    filial,
                    tipo,
                    codigo_evento,
                    agora.date(),
                    agora.time().replace(microsecond=0),
                ],
            )

    @staticmethod
    def excluir_evento(
        *,
        banco: str,
        db_alias: str = None,
        codigo_empresa: int = 1,
        codigo_filial: int = 1,
        even_tipo_calculo: str,
        even_codi,
    ):
        alias = db_alias or "default"
        banco_limpo = _digits_only(banco)
        empresa = int(codigo_empresa or 1)
        filial = int(codigo_filial or 1)
        tipo = _normalizar_tipo_calculo(even_tipo_calculo)
        codigo_evento = _safe_int(even_codi)

        if codigo_evento is None:
            raise ValidationError("Evento inválido para exclusão.")

        with connections[alias].cursor() as cur:
            cur.execute(
                "DELETE FROM eventos_automaticos "
                "WHERE registro = %s "
                "  AND even_empr = %s "
                "  AND even_fili = %s "
                "  AND even_tipo_calculo = %s "
                "  AND even_codi = %s",
                [banco_limpo, empresa, filial, tipo, codigo_evento],
            )
