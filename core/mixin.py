from django.http import Http404
from core.banco import get_banco_from_request
from core.utils import get_db_from_slug


class BancoObrigatorioMixin:
    def dispatch(self, request, *args, **kwargs):
        request.banco = get_banco_from_request(request)
        request.db_alias = get_db_from_slug(request.banco)

        return super().dispatch(request, *args, **kwargs)

    def get_banco_lookup(self):
        return {"registro": self.request.banco}

    def get_contextual_object(self, queryset, **lookup):
        filtros = self.get_banco_lookup()
        filtros.update(lookup)

        objeto = queryset.using(self.request.db_alias).filter(**filtros).first()

        if not objeto:
            raise Http404("Registro não encontrado.")

        return objeto