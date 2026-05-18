from django.db import connections
from folhamensal.models import Folhamensal

class ListarFolhaMensalService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Folhamensal.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Folhamensal.objects.using(db_alias).all().limit(100) 
