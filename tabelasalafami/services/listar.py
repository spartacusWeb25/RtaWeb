from tabelasalafami.models import Tabelasalafami    

class ListarTabelasalafamiService:
    def listar(*, banco : str, db_alias : str, referencia : str | None, ordenar: str | None = None):
        qs = Tabelasalafami.objects.using(db_alias)
        if referencia:
            qs = qs.filter(safa_refe__icontains=referencia.strip())

        if ordenar == "referencia":
            qs = qs.order_by("safa_refe")
        else:
            qs = qs.order_by("safa_refe")

        return qs[:100]
