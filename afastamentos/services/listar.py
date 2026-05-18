from django.db import connections
from afastamentos.models import Afastamentos


class ListarAfastamentosService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Afastamentos.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Afastamentos.objects.using(db_alias).all().limit(100)
