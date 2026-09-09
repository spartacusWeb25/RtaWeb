from django.db.models import Q
from contribuintes.models import Contribuintes


def _digits_only(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def listar_contribuintes(banco, db_alias, busca="", ordenacao="codigo_crescente"):
    banco_limpo = _digits_only(banco)
    qs = Contribuintes.objects.using(db_alias).filter(registro=banco_limpo)

    if busca:
        busca_upper = busca.upper()
        qs = qs.filter(
            Q(contr_nome__icontains=busca)
            | Q(contr_cpf__icontains=busca)
            | Q(contr_codi__icontains=busca)
        )

    ordem_map = {
        "codigo_crescente": "contr_codi",
        "codigo_decrescente": "-contr_codi",
        "nome_crescente": "contr_nome",
        "nome_decrescente": "-contr_nome",
        "asc": "contr_codi",
        "desc": "-contr_codi",
    }
    ordem = ordem_map.get(ordenacao, "contr_codi")
    qs = qs.order_by(ordem)

    return list(qs.all())


class ListarContribuintesService:
    """Wrapper de compatibilidade para apps (ex: dependentescontr) que importam
    essa classe em vez da função listar_contribuintes()."""

    @staticmethod
    def listar(banco, db_alias, busca="", ordenacao="codigo_crescente"):
        return listar_contribuintes(banco, db_alias, busca=busca, ordenacao=ordenacao)
