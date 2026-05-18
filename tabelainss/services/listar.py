from django.db import connections
from tabelainss.models import Tabelainss


class ListarTabelainssService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Tabelainss.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Tabelainss.objects.using(db_alias).all().limit(100)