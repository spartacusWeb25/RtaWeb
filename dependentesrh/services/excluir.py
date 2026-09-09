from dependentesrh.services.chave import DependentesChaveService


class DependentesExcluirService:

    @staticmethod
    def excluir(*, banco, db_alias, dados):
        dependente = DependentesChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

        if not dependente:
            raise ValueError("Dependente não encontrado.")

        DependentesChaveService.remover(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )
