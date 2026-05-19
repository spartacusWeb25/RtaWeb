from tabelasalafami.models import Tabelasalafami    

class ListarTabelasalafamiService:
    def listar(*, banco : str, db_alias : str, referencia : str | None):
        qs = Tabelasalafami.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(tabelasalafami__icontains=referencia.strip())
        return qs.order_by("tabelasalafami")[:100]
