from ferias.models import Ferias


class ListarFeriasService:
    def listar(*, banco: str, db_alias: str, referencia: str | None):
        qs = Ferias.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(registro__icontains=referencia.strip())
        return qs.order_by("-feri_refe", "registro")[:100]
        
