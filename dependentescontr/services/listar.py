from dependentescontr.models import Dependentescontr


class ListarDependentescontrService:
    @staticmethod
    def listar(
        *,
        banco: str,
        db_alias: str,
        empresa: str | None = None,
        filial: str | None = None,
        contribuinte: str | None = None,
        nome: str | None = None,
        cpf: str | None = None,
        codigo: str | None = None,
        invalido: str | None = None,
    ):
        qs = Dependentescontr.objects.using(db_alias).filter(registro=banco)

        if empresa:
            qs = qs.filter(depecontr_empr=empresa)
        if filial:
            qs = qs.filter(depecontr_fili=filial)
        if contribuinte:
            qs = qs.filter(depecontr_contr=contribuinte)
        if nome:
            qs = qs.filter(depecontr_nome__icontains=nome.strip())
        if cpf:
            qs = qs.filter(depecontr_cpf__icontains=cpf.strip())
        if codigo:
            qs = qs.filter(depecontr_codi=codigo)
        if invalido is not None and invalido != "":
            if invalido in ("1", "true", "True", "on", "sim", "s", "S", "SIM"):
                qs = qs.filter(depecontr_invalido=True)
            elif invalido in ("0", "false", "False", "nao", "não", "n", "N", "NAO", "NÃO"):
                qs = qs.filter(depecontr_invalido=False)

        return qs.order_by("depecontr_nome", "depecontr_codi")
