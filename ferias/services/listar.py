from django.db import connections
from ferias.models import Ferias


class ListarFeriasService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Ferias.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Ferias.objects.using(db_alias).all().limit(100)