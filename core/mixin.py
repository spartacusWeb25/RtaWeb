from core.utils import get_db_from_slug


class BancoObrigatorioMixin:
    def dispatch(self, request, *args, **kwargs):
        if not getattr(request, "banco", None):
            request.banco = "rta0001"

        request.db_alias = get_db_from_slug(request.banco)
        return super().dispatch(request, *args, **kwargs)
