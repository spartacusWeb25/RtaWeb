DEFAULT_BANCO_SLUG = "rta0001"


def get_db_from_slug(_slug=None):
    """
    Cenário atual: dados operacionais sempre no banco default.
    Mantemos a função por compatibilidade com o padrão do projeto.
    """
    return "default"


def get_default_banco_slug():
    return DEFAULT_BANCO_SLUG
