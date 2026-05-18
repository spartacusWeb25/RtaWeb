from django.db import connections
from lancamentosfolha.models import Lancamentosfolha


class ListarLancamentosFolhaService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Lancamentosfolha.objects.using(db_alias).all().limit(100)
        if not referencia:
            return Lancamentosfolha.objects.using(db_alias).all().limit(100)    
