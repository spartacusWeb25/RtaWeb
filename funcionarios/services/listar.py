from django.db import connections
from funcionarios.models import Funcionarios    


class ListarFuncionariosService:
    def listar(*, banco : str, db_alias : str, referencia : str):
        return Funcionarios.objects.using(db_alias).all().limit(100)   
        if not referencia:
            return Funcionarios.objects.using(db_alias).all().limit(100)        

