from tabelairrf.models import Tabelairrf


class ListarTabelairrfService:
    def listar(*, banco : str, db_alias : str, referencia : str | None):
        qs = Tabelairrf.objects.using(db_alias).all()
        if referencia:
            qs = qs.filter(irrf_refe__icontains=referencia.strip())
        return qs.order_by("-irrf_refe")[:100]
