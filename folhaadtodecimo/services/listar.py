from folhaadtodecimo.models import Folhaadtodecimo


class ListarFolhaAdtodecimoService:
    def listar(*, banco: str, db_alias: str, referencia: str | None):
        qs = Folhaadtodecimo.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(folhaadtodecimo__icontains=referencia.strip())
        return qs.order_by("folhaadtodecimo")[:100]
        
