from tabelasalafami.services.chave import TabelaSalaFamiChaveService


class SalaFamiEditarService:

    @staticmethod
    def editar(*, banco, db_alias, dados):
        salariofamilia = TabelaSalaFamiChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

        if not salariofamilia:
            raise ValueError("Salário familia não encontrado.")

        safa_refe = dados.get("safa_refe")
        if safa_refe and safa_refe != salariofamilia.safa_refe:
            raise ValueError("Não é permitido alterar a referência (safa_refe).")

        for campo in ("safa_fa01", "safa_co01", "safa_fa02", "safa_co02"):
            if campo in dados:
                setattr(salariofamilia, campo, dados.get(campo))

        salariofamilia.save(using=db_alias)

        return salariofamilia
