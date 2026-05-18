from setores.services.chave import SetoresChaveService


class SetoresExcluirService:

    @staticmethod
    def excluir(*, banco, db_alias, dados):
        setor = SetoresChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

        if not setor:
            raise ValueError("Setor não encontrado.")

        setor.delete(using=db_alias)