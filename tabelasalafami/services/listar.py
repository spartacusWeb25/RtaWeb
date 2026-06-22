from django.db.models import Q

from core.utils import get_month_reference_search_terms
from tabelasalafami.models import Tabelasalafami

class ListarTabelasalafamiService:
    def listar(*, banco: str, db_alias: str, referencia: str | None, ordenar: str | None = None):
        qs = Tabelasalafami.objects.using(db_alias)
        if referencia:
            filtros = Q()
            for termo in get_month_reference_search_terms(referencia):
                filtros |= Q(safa_refe__icontains=termo)
            qs = qs.filter(filtros)

        if ordenar == "referencia_desc":
            qs = qs.order_by("-safa_refe")
        elif ordenar == "referencia_asc":
            qs = qs.order_by("safa_refe")
        else:
            qs = qs.order_by("safa_refe")

        return qs[:100]
