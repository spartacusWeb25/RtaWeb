from eventos.models import Eventos


class ListarEventosService:
    def listar(*, banco: str, db_alias: str, referencia: str | None, ordenar: str | None = None):
        qs = Eventos.objects.using(db_alias).filter(registro=banco)

        if referencia:
            referencia = referencia.strip()
            if referencia.isdigit():
                qs = qs.filter(even_codi=int(referencia))
            else:
                qs = qs.filter(even_desc__icontains=referencia)

        if ordenar == "desc":
            qs = qs.order_by("-even_codi")
        elif ordenar == "desc_desc":
            qs = qs.order_by("-even_desc")
        elif ordenar == "desc_asc":
            qs = qs.order_by("even_desc")
        else:
            qs = qs.order_by("even_codi")

        return qs[:100]
        
