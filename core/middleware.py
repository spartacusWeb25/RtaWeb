from .banco import get_banco_from_request
from .utils import get_db_from_slug


class BancoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.banco = get_banco_from_request(request) or "rta0001"

        try:
            request.db_alias = get_db_from_slug(request.banco)
        except Exception:
            request.db_alias = "default"

        rotas_livres = (
            "/",
            "/licencas/login/",
            "/licencas/logout/",
            "/admin/",
            "/static/",
            "/favicon.ico",
        )

        if request.path.startswith(rotas_livres):
            return self.get_response(request)

        return self.get_response(request)
