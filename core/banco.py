from core.utils import get_default_banco_slug


def get_banco_from_request(request):
    return (
        request.GET.get("banco")
        or request.POST.get("banco")
        or request.session.get("banco")
        or request.headers.get("X-Banco")
        or get_default_banco_slug()
    )
