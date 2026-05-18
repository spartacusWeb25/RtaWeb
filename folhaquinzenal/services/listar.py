from django.db import connections
from folhaquinzenal.models import Folhaquinzenal 


class ListarFolhaQuinzenalService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Folhaquinzenal.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Folhaquinzenal.objects.using(db_alias).all().limit(100)  
