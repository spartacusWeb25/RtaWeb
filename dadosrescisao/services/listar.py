from dadosrescisao.models import Dadosrescisao


class ListarDadosRescisaoService:
    def listar(*, banco: str, db_alias: str, referencia: str | None):
        qs = Dadosrescisao.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(registro__icontains=referencia.strip())
        return qs.order_by("-dare_refe", "registro")[:100]
        
