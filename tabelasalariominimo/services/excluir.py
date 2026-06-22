from tabelasalariominimo.services.chave import TabelaSalarioMinimoChaveService


class SalarioMinimoExcluirService:

    @staticmethod
    def excluir(*, banco, db_alias, dados):
        salariominimo = TabelaSalarioMinimoChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

        if not salariominimo:
            raise ValueError("Salário mínimo não encontrado.")

        salariominimo.delete(using=db_alias)    
