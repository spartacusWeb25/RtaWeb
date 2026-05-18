from sindicatos.models import Sindicatos


class ListarSindicatosService:
    def listar(*, banco : str, db_alias : str, referencia : str | None):
        qs = Sindicatos.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(sindicatos__icontains=referencia.strip())
        return qs.order_by("sindicatos")[:100]
