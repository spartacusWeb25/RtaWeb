from django.db import connections
from empresas.models import Empresas


class ListarEmpresasService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Empresas.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Empresas.objects.using(db_alias).all().limit(100)