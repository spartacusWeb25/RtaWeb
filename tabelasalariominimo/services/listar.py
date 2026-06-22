from django.db.models import Q

from core.utils import get_month_reference_search_terms
from tabelasalariominimo.models import Tabelasalariominimo


class ListarTabelasalariominimoService:
    def listar(*, banco: str, db_alias: str, referencia: str | None, ordenar: str | None = None):
        qs = Tabelasalariominimo.objects.using(db_alias).all()
        if referencia:
            filtros = Q()
            for termo in get_month_reference_search_terms(referencia):
                filtros |= Q(refe_sala_mini__icontains=termo)
            qs = qs.filter(filtros)

        if ordenar == "referencia_desc":
            qs = qs.order_by("-refe_sala_mini")
        elif ordenar == "referencia_asc":
            qs = qs.order_by("refe_sala_mini")
        else:
            qs = qs.order_by("refe_sala_mini")

        return qs[:100]
