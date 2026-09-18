from django.db.models import Q
from terceiros.models import Terceiros


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def listar_terceiros(banco, db_alias, busca="", ordenacao="codigo_crescente"):
    banco_limpo = _digits_only(banco)
    qs = Terceiros.objects.using(db_alias).filter(registro=banco_limpo)

    if busca:
        busca_upper = busca.upper()
        qs = qs.filter(
            Q(terc_nome__icontains=busca)
            | Q(terc_codi__icontains=busca)
        )

    ordem_map = {
        "codigo_crescente": "terc_codi",
        "codigo_decrescente": "-terc_codi",
        "nome_crescente": "terc_nome",
        "nome_decrescente": "-terc_nome",
        "asc": "terc_codi",
        "desc": "-terc_codi",
    }
    ordem = ordem_map.get(ordenacao, "terc_codi")
    qs = qs.order_by(ordem)

    return list(qs.all())


class ListarTerceirosService:
    """Wrapper de compatibilidade para apps que importam
    essa classe em vez da função listar_terceiros()."""

    @staticmethod
    def listar(banco, db_alias, busca="", ordenacao="codigo_crescente"):
        return listar_terceiros(banco, db_alias, busca=busca, ordenacao=ordenacao)
