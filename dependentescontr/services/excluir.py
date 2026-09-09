from dependentescontr.services.chave import DependentescontrChaveService


class DependentescontrExcluirService:

    @staticmethod
    def excluir(*, banco, db_alias, dados):
        dependente = DependentescontrChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

        if not dependente:
            raise ValueError("Dependente de contribuinte não encontrado.")

        DependentescontrChaveService.remover(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )
