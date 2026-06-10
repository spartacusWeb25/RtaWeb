from horarios.models import Horarios


class ListarHorariosService:
    def listar(*, banco : str, db_alias : str, referencia : str | None):
        qs = Horarios.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(registro__icontains=referencia.strip())
        return qs.order_by("-hora_data", "hora_prof")[:100]
