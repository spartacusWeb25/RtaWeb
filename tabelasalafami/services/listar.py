from django.db import connections
from tabelasalafami.models import Tabelasalafami    

class ListarTabelasalafamiService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Tabelasalafami.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Tabelasalafami.objects.using(db_alias).all().limit(100)
