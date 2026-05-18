from django.db import connections
from licencas.models import Licencas

class ListarLicencasService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Licencas.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Licencas.objects.using(db_alias).all().limit(100)