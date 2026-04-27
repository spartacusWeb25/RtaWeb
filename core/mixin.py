from core.utils import get_db_from_slug
from django.http import Http404


class BancoObrigatorioMixin:
    def dispatch(self, request, *args, **kwargs):
        if not getattr(request, "banco", None):
            request.banco = "rta0001"

        request.db_alias = get_db_from_slug(request.banco)
        return super().dispatch(request, *args, **kwargs)

    def get_banco_lookup(self):
        return {"registro": self.request.banco}

    def get_contextual_object(self, queryset, **lookup):
        filtros = self.get_banco_lookup()
        filtros.update(lookup)
        objeto = queryset.filter(**filtros).first()
        if not objeto:
            raise Http404("Registro não encontrado.")
        return objeto
