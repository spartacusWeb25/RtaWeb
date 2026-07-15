from empresas.services.chave import EmpresasChaveService


class EmpresaExcluirService:

    @staticmethod
    def excluir(*, banco, db_alias, dados):
        empresa = EmpresasChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

        if not empresa:
            raise ValueError("Empresa nao encontrada.")

        deleted_count = EmpresasChaveService.remover(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )
        if not deleted_count:
            raise ValueError("Empresa nao encontrada.")
