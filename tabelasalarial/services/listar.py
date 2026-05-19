from tabelasalarial.models import Tabelasalarial    


class ListarTabelasalarialService:
    def listar(*, banco : str, db_alias : str, referencia : str | None):
        qs = Tabelasalarial.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(tabelasalarial__icontains=referencia.strip())
        return qs.order_by("tabelasalarial")[:100]
