from django.db import connections
from cargos.models import Cargos


class ListarCargosService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Cargos.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Cargos.objects.using(db_alias).all().limit(100)