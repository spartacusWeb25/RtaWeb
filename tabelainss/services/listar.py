from tabelainss.models import Tabelainss


class ListarTabelainssService:
    def listar(*, banco : str, db_alias : str, referencia : str | None):
        qs = Tabelainss.objects.using(db_alias).all()
        if referencia:
            qs = qs.filter(tabe_refe__icontains=referencia.strip())
        return qs.order_by("-tabe_refe")[:100]
