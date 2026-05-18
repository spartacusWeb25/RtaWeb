from django.db import connections
from adtodecimo.models import Adtodecimo


class ListarAdtoDecimoService:
    def listar(*, banco : str, db_alias : str, referencia : str):   
        return Adtodecimo.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Adtodecimo.objects.using(db_alias).all().limit(100)
            
