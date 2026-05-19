from dadosrescisao.models import Dadosrescisao


class ListarDadosRescisaoService:
    def listar(*, banco: str, db_alias: str, referencia: str | None):
        qs = Dadosrescisao.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(dadosrescisao__icontains=referencia.strip())
        return qs.order_by("dadosrescisao")[:100]
        
