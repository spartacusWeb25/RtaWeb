from afastamentos.models import Afastamentos


class ListarAfastamentosService:
    def listar(*, banco: str, db_alias: str, referencia: str | None):
        qs = Afastamentos.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(registro__icontains=referencia.strip())
        return qs.order_by("-afas_said", "registro")[:100]
        

