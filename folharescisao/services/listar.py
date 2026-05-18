from django.db import connections
from folharescisao.models import Folharescisao  


class ListarFolhaRescisaoService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Folharescisao.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Folharescisao.objects.using(db_alias).all().limit(100)
