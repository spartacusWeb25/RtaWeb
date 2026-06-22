from django.db.models import Q

from core.utils import get_month_reference_search_terms
from tabelairrf.models import Tabelairrf


class ListarTabelairrfService:
    def listar(*, banco: str, db_alias: str, referencia: str | None, ordenar: str | None = None):
        qs = Tabelairrf.objects.using(db_alias).all()
        if referencia:
            filtros = Q()
            for termo in get_month_reference_search_terms(referencia):
                filtros |= Q(irrf_refe__icontains=termo)
            qs = qs.filter(filtros)

        if ordenar == "referencia_desc":
            qs = qs.order_by("-irrf_refe")
        elif ordenar == "referencia_asc":
            qs = qs.order_by("irrf_refe")
        else:
            qs = qs.order_by("irrf_refe")

        return qs[:100]
