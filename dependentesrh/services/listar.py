from dependentesrh.models import Dependentesrh


class ListarDependentesrhService:
    @staticmethod
    def listar(
        *,
        banco: str,
        db_alias: str,
        empresa: str | None = None,
        filial: str | None = None,
        funcionario: str | None = None,
        nome: str | None = None,
        cpf: str | None = None,
        codigo: str | None = None,
        invalido: str | None = None,
    ):
        qs = Dependentesrh.objects.using(db_alias).filter(registro=banco)

        if empresa:
            qs = qs.filter(depe_empr=empresa)
        if filial:
            qs = qs.filter(depe_fili=filial)
        if funcionario:
            qs = qs.filter(depe_func=funcionario)
        if nome:
            qs = qs.filter(depe_nome__icontains=nome.strip())
        if cpf:
            qs = qs.filter(depe_cpf__icontains=cpf.strip())
        if codigo:
            qs = qs.filter(depe_codi=codigo)
        if invalido is not None and invalido != "":
            if invalido in ("1", "true", "True", "on"):
                qs = qs.filter(depe_invalido=True)
            elif invalido in ("0", "false", "False"):
                qs = qs.filter(depe_invalido=False)

        return qs.order_by("depe_nome", "depe_codi")
