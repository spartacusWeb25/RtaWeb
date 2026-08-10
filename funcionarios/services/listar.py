from funcionarios.models import Funcionarios


class ListarFuncionariosService:
    def listar(*, banco: str, db_alias: str, referencia: str | None, ordenar: str | None = None):
        qs = Funcionarios.objects.using(db_alias).filter(registro=banco)

        if referencia:
            qs = qs.filter(func_nome__icontains=referencia.strip())

        if ordenar == "desc":
            qs = qs.order_by("-func_nome", "-func_codi")
        else:
            qs = qs.order_by("func_nome", "func_codi")

        return qs[:100]

