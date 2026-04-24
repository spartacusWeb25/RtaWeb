from .banco import get_banco_from_request

class BancoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.banco = get_banco_from_request(request)
        return self.get_response(request)