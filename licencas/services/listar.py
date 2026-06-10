from django.db import connections
from licencas.models import Licencas

class ListarLicencasService:
    def listar(*, banco: str, db_alias: str, referencia: str | None):
        qs = Licencas.objects.using(db_alias).all()
        if referencia:
            qs = qs.filter(lice_nome__icontains=referencia.strip())
        return qs.order_by("lice_nome")[:100]