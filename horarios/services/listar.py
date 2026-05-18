from django.db import connections
from horarios.models import Horarios


class ListarHorariosService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Horarios.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Horarios.objects.using(db_alias).all().limit(100)