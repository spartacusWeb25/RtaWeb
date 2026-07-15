from core.utils import get_default_banco_slug


def get_banco_from_request(request):
    banco_sessao = request.session.get("banco")

    # After login, the active license stored in session becomes the source of truth.
    if request.session.get("usuario_id") and banco_sessao:
        return banco_sessao

    return (
        banco_sessao
        or request.GET.get("banco")
        or request.POST.get("banco")
        or request.headers.get("X-Banco")
        or get_default_banco_slug()
    )
