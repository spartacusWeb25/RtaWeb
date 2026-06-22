class TabelaSalarioMinimoChaveService:
    CAMPOS_CHAVE = [
        "refe_sala_mini",
    ]

    @staticmethod
    def montar_chave(*, banco, dados):
        return {
            "refe_sala_mini": dados.get("refe_sala_mini"),
        }

    @staticmethod
    def existe(*, banco, db_alias, dados):
        from tabelasalariominimo.models import Tabelasalariominimo

        chave = TabelaSalarioMinimoChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return False

        return Tabelasalariominimo.objects.using(db_alias).filter(**chave).exists()

    @staticmethod
    def buscar(*, banco, db_alias, dados):
        from tabelasalariominimo.models import Tabelasalariominimo

        chave = TabelaSalarioMinimoChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return None

        return Tabelasalariominimo.objects.using(db_alias).filter(**chave).first()
   
    @staticmethod
    def remover(*, banco, db_alias, dados):
        from tabelasalariominimo.models import Tabelasalariominimo

        chave = TabelaSalarioMinimoChaveService.montar_chave(
            banco=banco,
            dados=dados,
        )

        if not all(chave.values()):
            return

        Tabelasalariominimo.objects.using(db_alias).filter(**chave).delete()

    
