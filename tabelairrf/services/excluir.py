from tabelairrf.services.chave import TabelaIrrfChaveService


class TabelaIrrfExcluirService:
    @staticmethod
    def excluir(*, banco, db_alias, dados):
        tabelairrf = TabelaIrrfChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

        if not tabelairrf:
            raise ValueError("Tabela IRRF não encontrada.")

        tabelairrf.delete(using=db_alias)
