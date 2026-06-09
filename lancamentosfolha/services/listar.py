from lancamentosfolha.models import Lancamentosfolha


class ListarLancamentosFolhaService:
    def listar(*, banco : str, db_alias : str, referencia : str | None):
        qs = Lancamentosfolha.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(registro__icontains=referencia.strip())
        return qs.order_by("-lafo_refe", "registro")[:100]    
