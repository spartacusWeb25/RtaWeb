from django.db import connections
from usuarios.models import Usuarios


class ListarUsuariosService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Usuarios.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Usuarios.objects.using(db_alias).all().limit(100)