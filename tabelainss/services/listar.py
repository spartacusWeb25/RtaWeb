from tabelainss.models import Tabelainss


class ListarTabelainssService:
    def listar(*, banco : str, db_alias : str, referencia : str | None):
        qs = Tabelainss.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(tabelainss__icontains=referencia.strip())
        return qs.order_by("tabelainss")[:100]
