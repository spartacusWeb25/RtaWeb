from django.db import connections
from sindicatos.models import Sindicatos


class ListarSindicatosService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Sindicatos.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Sindicatos.objects.using(db_alias).all().limit(100)