from sindicatos.models import Sindicatos
from sindicatos.services.logic import _digits_only


class ListarSindicatosService:

    @staticmethod
    def listar(banco, db_alias, referencia=None, ordenar="asc"):
        banco_limpo = _digits_only(banco)
        qs = Sindicatos.objects
        if db_alias:
            qs = qs.using(db_alias)
        qs = qs.filter(registro=banco_limpo)

        ref = (referencia or "").strip()
        if ref:
            if ref.isdigit():
                qs = qs.filter(sind_codi=int(ref))
            else:
                qs = qs.filter(sind_nome__icontains=ref)

        if str(ordenar).lower() == "desc":
            qs = qs.order_by("-sind_empr", "-sind_fili", "-sind_codi")
        else:
            qs = qs.order_by("sind_empr", "sind_fili", "sind_codi")

        return list(qs)
