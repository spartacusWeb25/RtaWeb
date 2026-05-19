from tabelairrf.models import Tabelairrf


class ListarTabelairrfService:
    def listar(*, banco : str, db_alias : str, referencia : str | None):
        qs = Tabelairrf.objects.using(db_alias).all().limit(100)
        if referencia:
            qs = qs.filter(tabelairrf__icontains=referencia.strip())
        return qs.order_by("tabelairrf")[:100]
