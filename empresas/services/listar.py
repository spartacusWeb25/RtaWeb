from empresas.models import Empresas


class ListarEmpresasService:
    def listar(*, banco: str, db_alias: str, referencia: str | None):
        qs = Empresas.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(empresa__icontains=referencia.strip())
        return qs.order_by("empresa")[:100]
        
