from django.db import connections
from dadosrescisao.models import Dadosrescisao


class ListarDadosRescisaoService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Dadosrescisao.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Dadosrescisao.objects.using(db_alias).all().limit(100)