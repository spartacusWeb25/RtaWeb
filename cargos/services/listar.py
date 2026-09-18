from cargos.models import Cargos
from cargos.services.logic import _digits_only


class ListarCargosService:

    _ORDENACAO_MAP = {
        "asc": ["carg_codi"],
        "desc": ["-carg_codi"],
    }

    @staticmethod
    def listar(*, banco: str, db_alias: str, referencia=None, ordenar="asc"):
        banco_limpo = _digits_only(banco)
        qs = Cargos.objects.using(db_alias).filter(registro=banco_limpo)
        if referencia:
            ref = referencia.strip()
            if ref.isdigit():
                try:
                    qs = qs.filter(carg_codi=int(ref))
                except Exception:
                    pass
            else:
                qs = qs.filter(carg_descricao__icontains=ref)
        order_fields = ListarCargosService._ORDENACAO_MAP.get(
            ordenar,
            ListarCargosService._ORDENACAO_MAP["asc"],
        )
        return qs.order_by(*order_fields)
