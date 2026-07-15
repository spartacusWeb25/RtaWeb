from django.db.models import Q

from empresas.models import Empresas


class ListarEmpresasService:
    def listar(*, banco: str, db_alias: str, referencia: str | None, ordenar: str | None = None):
        qs = Empresas.objects.using(db_alias).filter(registro=banco)

        if referencia:
            termo = referencia.strip()
            qs = qs.filter(Q(empr_nome__icontains=termo))

        if ordenar == "desc":
            qs = qs.order_by("-empr_empr", "-empr_fili")
        else:
            qs = qs.order_by("empr_empr", "empr_fili")

        return qs[:100]
