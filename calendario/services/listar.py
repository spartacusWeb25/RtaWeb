from django.db import connections
from calendario.models import Calendariorh


class ListarCalendarioService:
    def listar(*, banco: str, db_alias: str, referencia: str | None):
        qs = Calendariorh.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(cale_refe__icontains=referencia.strip())
        return qs.order_by("-cale_data", "registro")[:100]