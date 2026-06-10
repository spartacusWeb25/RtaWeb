from adtodecimo.models import Adtodecimo


class ListarAdtoDecimoService:
    def listar(*, banco: str, db_alias: str, referencia: str | None):
        qs = Adtodecimo.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(registro__icontains=referencia.strip())
        return qs.order_by("-adto_ano", "registro")[:100]
        
            
