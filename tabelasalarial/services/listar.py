from django.db import connections
from tabelasalarial.models import Tabelasalarial    


class ListarTabelasalarialService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Tabelasalarial.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Tabelasalarial.objects.using(db_alias).all().limit(100)