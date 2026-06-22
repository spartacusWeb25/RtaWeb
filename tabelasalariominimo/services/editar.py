from tabelasalariominimo.services.chave import TabelaSalarioMinimoChaveService


class SalarioMinimoEditarService:

    @staticmethod
    def editar(*, banco, db_alias, dados):
        salariominimo = TabelaSalarioMinimoChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados=dados,
        )

        if not salariominimo:
            raise ValueError("Salário mínimo não encontrado.")

        refe_sala_mini = dados.get("refe_sala_mini")
        if refe_sala_mini and refe_sala_mini != salariominimo.refe_sala_mini:
            raise ValueError("Não é permitido alterar a referência (refe_sala_mini).")

        for campo in ("refe_sala_mini_fede",):
            if campo in dados:
                setattr(salariominimo, campo, dados.get(campo))

        salariominimo.save(using=db_alias)

        return salariominimo
