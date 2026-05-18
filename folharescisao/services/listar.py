from folharescisao.models import Folharescisao  


class ListarFolhaRescisaoService:
    def listar(*, banco : str, db_alias : str, referencia : str | None):
        qs = Folharescisao.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(folharescisao__icontains=referencia.strip())
        return qs.order_by("folharescisao")[:100]
