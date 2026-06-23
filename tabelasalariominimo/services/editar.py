from tabelasalariominimo.services.chave import TabelaSalarioMinimoChaveService
from tabelasalariominimo.models import Tabelasalariominimo


class SalarioMinimoEditarService:

    @staticmethod
    def editar(*, banco, db_alias, dados):
        dados = dict(dados)
        refe_original = dados.pop("_original_refe_sala_mini", None) or dados.get("refe_sala_mini")

        salariominimo = TabelaSalarioMinimoChaveService.buscar(
            banco=banco,
            db_alias=db_alias,
            dados={"refe_sala_mini": refe_original},
        )

        if not salariominimo:
            raise ValueError("Salário mínimo não encontrado.")

        valores_atualizados = {}
        for campo in ("refe_sala_mini", "refe_sala_mini_fede"):
            if campo in dados:
                valores_atualizados[campo] = dados.get(campo)

        if not valores_atualizados:
            return salariominimo

        Tabelasalariominimo.objects.using(db_alias).filter(refe_sala_mini=refe_original).update(**valores_atualizados)

        return Tabelasalariominimo.objects.using(db_alias).get(refe_sala_mini=valores_atualizados.get("refe_sala_mini", refe_original))
