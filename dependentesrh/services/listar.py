from dependentesrh.models import Dependentesrh


class ListarDependentesRhService:
    def listar(*, banco: str, db_alias: str, referencia: str | None):
        qs = Dependentesrh.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(dependente__icontains=referencia.strip())
        return qs.order_by("dependente")[:100]
        
