from tabelasalafami.models import Tabelasalafami    

class ListarTabelasalafamiService:
    def listar(*, banco : str, db_alias : str, referencia : str | None):
        qs = Tabelasalafami.objects.using(db_alias)
        if referencia:
            qs = qs.filter(safa_refe__icontains=referencia.strip())
        
        return qs.order_by("safa_refe")[:100]
