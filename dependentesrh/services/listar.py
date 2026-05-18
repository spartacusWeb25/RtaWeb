from django.db import connections
from dependentesrh.models import Dependentesrh


class ListarDependentesRhService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Dependentesrh.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Dependentesrh.objects.using(db_alias).all().limit(100)