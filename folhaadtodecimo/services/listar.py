from django.db import connections
from folhaadtodecimo.models import Folhaadtodecimo


class ListarFolhaAdtodecimoService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Folhaadtodecimo.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Folhaadtodecimo.objects.using(db_alias).all().limit(100)