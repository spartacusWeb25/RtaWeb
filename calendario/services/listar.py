from django.db import connections
from calendario.models import Calendariorh


class ListarCalendarioService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Calendariorh.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Calendariorh.objects.using(db_alias).all().limit(100)