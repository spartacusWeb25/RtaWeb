from .banco import get_banco_from_request
from .utils import get_db_from_slug


class BancoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.banco = get_banco_from_request(request)
        request.db_alias = get_db_from_slug(request.banco)
        return self.get_response(request)
