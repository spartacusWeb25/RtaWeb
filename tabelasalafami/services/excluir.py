from tabelasalafami.services.chave import TabelaSalaFamiChaveService


class SalaFamiExcluirService:

    @staticmethod
    def excluir(*, banco, db_alias, dados):
        salariofamilia = TabelaSalaFamiChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

        if not salariofamilia:
            raise ValueError("Salário familia não encontrado.")

        salariofamilia.delete(using=db_alias)   
