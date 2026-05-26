from tabelasalariominimo.models import Tabelasalariominimo  
  
        
class ListarTabelasalariominimoService:
    def listar(*, banco : str, db_alias : str, referencia : str | None):
        qs = Tabelasalariominimo.objects.using(db_alias).filter(registro__startswith=banco)
        if referencia:
            qs = qs.filter(registro__icontains=referencia.strip())
        return qs.order_by("-registro")[:100]
