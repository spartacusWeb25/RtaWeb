from django.db import connections
from tabelasalariominimo.models import Tabelasalariominimo  
  
        
class ListarTabelasalariominimoService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Tabelasalariominimo.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Tabelasalariominimo.objects.using(db_alias).all().limit(100)