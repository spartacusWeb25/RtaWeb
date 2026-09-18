from sindicatospatronais.models import SindicatosPatronais
from sindicatospatronais.services.logic import _digits_only


_ORDENACAO_MAP = {
    "codigo_crescente": ["sind_empr", "sind_fili", "sind_codi"],
    "codigo_decrescente": ["-sind_empr", "-sind_fili", "-sind_codi"],
    "nome_crescente": ["sind_nome"],
    "nome_decrescente": ["-sind_nome"],
}


class ListarSindicatosPatronaisService:

    @staticmethod
    def listar(banco, db_alias, referencia=None, ordenacao="codigo_crescente"):
        banco_limpo = _digits_only(banco)
        qs = SindicatosPatronais.objects
        if db_alias:
            qs = qs.using(db_alias)
        qs = qs.filter(registro=banco_limpo)

        ref = (referencia or "").strip()
        if ref:
            if ref.isdigit():
                qs = qs.filter(sind_codi=int(ref))
            else:
                qs = qs.filter(sind_nome__icontains=ref)

        order_fields = _ORDENACAO_MAP.get(ordenacao, _ORDENACAO_MAP["codigo_crescente"])
        qs = qs.order_by(*order_fields)
        return list(qs)
