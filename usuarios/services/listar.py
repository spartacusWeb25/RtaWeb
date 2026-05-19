from usuarios.models import Usuarios


class ListarUsuariosService:
    def listar(*, banco : str, db_alias : str, referencia : str | None):
        qs = Usuarios.objects.using(db_alias).filter(registro=banco)
        if referencia:
            qs = qs.filter(usuarios__icontains=referencia.strip())
        return qs.order_by("usuarios")[:100]
