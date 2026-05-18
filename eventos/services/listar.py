from django.db import connections
from eventos.models import Eventos


class ListarEventosService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Eventos.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Eventos.objects.using(db_alias).all().limit(100)