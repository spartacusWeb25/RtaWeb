from cargos.models import Cargos


class ListarCargosService:
    def listar(*, banco: str, db_alias: str, referencia: str | None):
        qs = Cargos.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(carg_nome__icontains=referencia.strip())
        return qs.order_by("carg_nome", "registro")[:100]
        
