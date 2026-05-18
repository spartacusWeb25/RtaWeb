from eventos.models import Eventos


class ListarEventosService:
    def listar(*, banco: str, db_alias: str, referencia: str | None):
        qs = Eventos.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(evento__icontains=referencia.strip())
        return qs.order_by("evento")[:100]
        
