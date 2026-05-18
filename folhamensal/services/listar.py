from folhamensal.models import Folhamensal


class ListarFolhaMensalService:

    LIMITE_MAXIMO = 100

    @staticmethod
    def listar(
        *,
        banco,
        db_alias,
        referencia=None,
        empresa=None,
        filial=None,
        funcionario=None,
        evento=None,
        ordenar=None,
    ):

        qs = Folhamensal.objects.using(db_alias).filter(
            registro=banco
        )

        if referencia:
            qs = qs.filter(fome_refe=referencia)

        if empresa:
            qs = qs.filter(fome_empr=empresa)

        if filial:
            qs = qs.filter(fome_fili=filial)

        if funcionario:
            qs = qs.filter(fome_func=funcionario)

        if evento:
            qs = qs.filter(fome_even=evento)

        ordenacoes = {
            "referencia": "fome_refe",
            "referencia_desc": "-fome_refe",
            "funcionario": "fome_func",
            "evento": "fome_even",
            "valor": "fome_valo",
            "valor_desc": "-fome_valo",
        }

        campo = ordenacoes.get(ordenar, "fome_func")

        return qs.order_by(campo)[:ListarFolhaMensalService.LIMITE_MAXIMO]