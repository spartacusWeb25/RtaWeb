from dependentesterc.services.chave import DependentestercChaveService


class DependentestercExcluirService:

    @staticmethod
    def excluir(*, banco, db_alias, dados):
        dependente = DependentestercChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

        if not dependente:
            raise ValueError("Dependente de terceiro não encontrado.")

        DependentestercChaveService.remover(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )
