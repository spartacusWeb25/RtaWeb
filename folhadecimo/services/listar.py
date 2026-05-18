from django.db import connections
from folhadecimo.models import Folhadecimo


class ListarFolhadDecimoService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Folhadecimo.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Folhadecimo.objects.using(db_alias).all().limit(100)