from django.shortcuts import redirect
from django.urls import reverse

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

        rotas_livres_exatas = {
            "/",
            "/favicon.ico",
        }
        rotas_livres_prefixos = (
            "/licencas/login/",
            "/licencas/logout/",
            "/admin/",
            "/static/",
        )

        if request.path in rotas_livres_exatas or request.path.startswith(rotas_livres_prefixos):
            return self.get_response(request)

        if not request.session.get("usuario_id"):
            login_url = reverse("licencas:login")
            destino = request.get_full_path()
            if destino and destino != "/":
                return redirect(f"{login_url}?next={destino}")
            return redirect(login_url)

        return self.get_response(request)
