from tabelainss.services.chave import TabelaInssChaveService


class TabelaInssExcluirService:

    @staticmethod
    def excluir(*, banco, db_alias, dados):
        tabelainss = TabelaInssChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

        if not tabelainss:
            raise ValueError("Tabela INSS não encontrado.")

        tabelainss.delete(using=db_alias)    
