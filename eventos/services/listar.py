from eventos.models import Eventos


class ListarEventosService:
    def listar(*, banco: str, db_alias: str, referencia: str | None):
        qs = Eventos.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(even_desc__icontains=referencia.strip())
        return qs.order_by("even_codi", "registro")[:100]
        
