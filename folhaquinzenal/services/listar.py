from folhaquinzenal.models import Folhaquinzenal 


class ListarFolhaQuinzenalService:
    def listar(*, banco : str, db_alias : str, referencia : str | None):
        qs = Folhaquinzenal.objects.using(db_alias).all().limit(100)
        if referencia:
            qs = qs.filter(folhaquinzenal__icontains=referencia.strip())
        return qs.order_by("folhaquinzenal")[:100]
