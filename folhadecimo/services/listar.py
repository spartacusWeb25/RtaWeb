from folhadecimo.models import Folhadecimo


class ListarFolhadDecimoService:
    def listar(*, banco : str, db_alias : str, referencia : str | None):
        qs = Folhadecimo.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(folhadecimo__icontains=referencia.strip())
        return qs.order_by("folhadecimo")[:100]
