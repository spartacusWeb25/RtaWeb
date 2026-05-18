from django.db import connections
from tabelairrf.models import Tabelairrf


class ListarTabelairrfService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Tabelairrf.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Tabelairrf.objects.using(db_alias).all().limit(100)